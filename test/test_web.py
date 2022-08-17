import unittest
from unittest.mock import MagicMock, patch
from xml.etree import ElementTree as ET

import extractor
import main
import sample_data
from model import Video


class FlaskTest(unittest.TestCase):

    def setUp(self):
        main.app.config["TESTING"] = True
        self.app = main.app.test_client()


class TestEntryPoints(FlaskTest):

    @patch(
        "main.from_tiktok_url",
        return_value=""
    )
    def test_link_detection(self, mock: MagicMock):
        for request_path, expected_url in {
            # vm share links
            sample_data.vm_code_working: sample_data.vm_base + sample_data.vm_code_working,
            sample_data.vm_code_working + "/": sample_data.vm_base + sample_data.vm_code_working,
            # "regular" urls (username+id)
            sample_data.www_path_working: sample_data.www_base + sample_data.www_path_working,
            sample_data.www_path_working + "/": sample_data.www_base + sample_data.www_path_working,
        }.items():
            with self.subTest(request_path=request_path, expected_url=expected_url):
                r = self.app.get(request_path)
                self.assertEqual(r.status_code, 200)
                mock.assert_called_once_with(expected_url)
                mock.reset_mock()


class TestWebOutput(FlaskTest):

    def test_proxy_url_generation(self):
        base_url = "http://foo/bar"
        for existing_params, expected_params in (
                ({}, "?direct=True"),
                ({"foo": "bar"}, "?foo=bar&direct=True"),
                ({"bar": "foo"}, "?bar=foo&direct=True"),
                ({"foo": " ?"}, "?foo=+%3F&direct=True"),
                ({"direct": "True"}, "?direct=True"),
                ({"direct": "False"}, "?direct=True"),
        ):
            with self.subTest(existing_params=existing_params, expected_params=expected_params):
                self.assertEqual(main.get_proxy_url(base_url, existing_params), base_url + expected_params)

    @patch(
        "main.extractor.extract_info",
        return_value=sample_data.video
    )
    @patch(
        "main.get_proxy_url",
        return_value="https://some.proxy/url"
    )
    def test_embed_og_tags(self, mock_proxy: MagicMock, mock_extract: MagicMock):
        # doesn't have to be a working vm code
        r = self.app.get("asdasd")
        self.assertEqual(r.status_code, 200)
        root = ET.fromstring(r.text)
        tags = {}
        for meta in root.find("head").findall("meta"):
            try:
                prop = meta.attrib["property"]
                content = meta.attrib["content"]
            except KeyError:
                continue
            tags[prop.removeprefix("og:")] = content
        video: Video = mock_extract.return_value
        url: str = mock_proxy.return_value
        self.assertEqual(tags["type"], "video.other")
        self.assertEqual(tags["video:type"], "video/mp4")
        self.assertEqual(tags["title"], video.author)
        self.assertEqual(tags["site_name"], video.title)
        self.assertEqual(tags["video:width"], str(video.width))
        self.assertEqual(tags["video:height"], str(video.height))
        self.assertEqual(tags["video:secure_url"], url)
        self.assertEqual(tags["video"], url)

    @patch(
        "main.extractor.extract_info",
        return_value=sample_data.video
    )
    def test_direct_redirect(self, mock: MagicMock):
        r = self.app.get("asdasd?direct=True")
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.headers["Location"], mock.return_value.url)
