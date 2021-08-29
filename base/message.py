import io
import abc
import sys
import json
import socket
import struct

from typing import Dict


class MessageMixin(abc.ABC):

    def create_message(self, obj: Dict) -> bytes:
        return self._create_message(
            content_bytes=self._json_encode(obj=obj, encoding='utf-8')
        )

    def _create_message(self, content_bytes: bytes) -> bytes:
        encoding = 'utf-8'
        header = {
            'byteorder': sys.byteorder,
            'content-length': len(content_bytes),
            'content-type': 'text/json',
            'content-encoding': encoding
        }

        header_bytes = self._json_encode(obj=header, encoding=encoding)
        message_header = struct.pack('>H', len(header_bytes))
        return message_header + header_bytes + content_bytes

    def read_message(self, sock: socket.socket) -> Dict:
        header_len = 2
        recv_data = sock.recv(header_len)
        if recv_data:
            json_length = struct.unpack('>H', recv_data)[0]
            header = self._get_json_header(sock, json_length)
            if header:
                data = self._process_header(sock, header)
                return data

    def _get_json_header(self, sock: socket.socket,
                         header_length: int) -> Dict:
        recv_data = sock.recv(header_length)
        if recv_data and len(recv_data) == header_length:
            json_data = self._json_decode(recv_data, encoding='utf-8')
            return json_data

    def _process_header(self, sock: socket.socket, header: Dict) -> Dict:
        if header['content-type'] == 'text/json':
            content_length = header['content-length']
            encoding = header['content-encoding']
            content_bytes = sock.recv(content_length)
            json_data = self._json_decode(content_bytes, encoding=encoding)
            return json_data

    @staticmethod
    def _json_encode(obj: Dict, encoding: str) -> bytes:
        return json.dumps(obj=obj, ensure_ascii=False).encode(
            encoding=encoding)

    @staticmethod
    def _json_decode(json_bytes: bytes, encoding: str) -> Dict:
        wrapper = io.TextIOWrapper(
            io.BytesIO(json_bytes), encoding=encoding, newline=''
        )
        obj = json.load(wrapper)
        wrapper.close()
        return obj
