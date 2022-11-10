import urllib.parse

from flask import Flask, abort, redirect, render_template, request

import extractor

app = Flask(__name__)


@app.get("/favicon.ico")
def favicon():
    abort(404)


@app.get("/@<username>/video/<video_id>")
@app.get("/@<username>/video/<video_id>/")
def oddly_specific(username, video_id):
    return from_tiktok_url(f"https://www.tiktok.com/@{username}/video/{video_id}")


@app.get("/<share_code>")
@app.get("/<share_code>/")
def vm_share(share_code):
    return from_tiktok_url(f"https://vm.tiktok.com/{share_code}")


def from_tiktok_url(url):
    data = extractor.extract_info(url)
    if request.args.get("direct"):
        return redirect(data.url, code=302)
    if request.args.get("original"):
        return redirect(url, code=302)
    return render_template(
        "embed.html",
        video=data,
        # TODO research after how long the direct urls go down
        # it might not be necessary to keep the url updated this way, but I've had a video go unreachable before.
        # The server/tunnel wasn't running anymore though, so discord re-fetching the embed after cache expiration
        # might just be enough. who knows ¯\_(ツ)_/¯
        url=get_proxy_url(request.base_url, request.args | dict(direct=True)),
        original_url=get_proxy_url(
            request.base_url, request.args | dict(original=True))
    )


def get_proxy_url(base_url, query_params):
    return base_url + "?" + urllib.parse.urlencode(query_params)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
