import os
import re
from flask import Flask
from flask_api import FlaskAPI
from flask import Flask, request, jsonify, make_response, json
from instance.config import app_config
from dotenv import load_dotenv
from flask_cors import CORS
from converter import Converter


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['PROPAGATE_EXCEPTIONS'] = True
    CORS(app)


    @app.route('/', methods=['GET'])
    def welcome_to_api():
        response = {"status": 200, "message": "Welcome To Manorlds Video Converter API."}
        return make_response(jsonify(response)), 200


    
    @app.route('/upload', methods=['POST'])
    def upload_video():
        try:
            original_file = request.files['le_file']
            if original_file:

                print(type(original_file))

                # return make_response(jsonify({"status": 200, "message": original_file.content_type})), 400

                try:
                    ffmpegPath = r"E:/VideoConverter/api/ffmpeg_win/bin/ffmpeg.exe"
                    ffprobePath = r"E:/VideoConverter/api/ffmpeg_win/bin/ffprobe.exe"

                    conv = Converter(ffmpeg_path = ffmpeg_path, ffprobe_path=ffprobe_path)
                    info = conv.probe(original_file)
                    convert = conv.convert(original_file, 'E:/VideoConverter/test1.mp4', {
                                'format': 'mp4',
                                'audio': {
                                    'codec': 'aac',
                                    'samplerate': 11025,
                                    'channels': 2
                                },
                                'video': {
                                    'codec': 'hevc',
                                    'width': 720,
                                    'height': 400,
                                    'fps': 25
                        }})

                    for timecode in convert:
                        print(f'\rConverting ({timecode:.2f}) ...')

                    response = {"status": 200, "message": "Video uploaded"}
                    return make_response(jsonify(response)), 200

                except KeyError as error:
                    return make_response(jsonify({"status": 400, "error": error})), 400

            else:
                response = {"status": 400, "message": "Upload file first"}
                return make_response(jsonify(response)), 400
        except KeyError:
            return make_response(jsonify({"status": 400, "message": "Upload File First"})), 400
        



    return app