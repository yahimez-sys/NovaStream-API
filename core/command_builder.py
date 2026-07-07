import os


class CommandBuilder:

    @staticmethod
    def build(job, output_path):

        command = [

            "yt-dlp",

            "--newline",

            "--no-warnings",

            "--ignore-errors",

            "--continue",

            "--retries", "10",

            "--fragment-retries", "10",

            "--concurrent-fragments", "8",

            "--socket-timeout", "30",

            "--no-playlist",

        ]

        # ============================
        # Formato
        # ============================

        if job.quality == "audio":

            command += [

                "-f",

                "bestaudio/best",

                "--extract-audio",

                "--audio-format",

                "mp3",

                "--audio-quality",

                "0"

            ]

        else:

            formats = {

                "360": "bestvideo[height<=360]+bestaudio/best",

                "480": "bestvideo[height<=480]+bestaudio/best",

                "720": "bestvideo[height<=720]+bestaudio/best",

                "1080": "bestvideo[height<=1080]+bestaudio/best",

                "1440": "bestvideo[height<=1440]+bestaudio/best",

                "4k": "bestvideo[height<=2160]+bestaudio/best",

                "best": "bestvideo+bestaudio/best"

            }

            command += [

                "-f",

                formats.get(job.quality, formats["best"]),

                "--merge-output-format",

                "mp4"

            ]

        # ============================
        # Salida
        # ============================

        command += [

            "-o",

            output_path

        ]

        # URL

        command.append(job.url)

        return command