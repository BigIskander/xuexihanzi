if __name__ == '__main__':
    import sys
    from google_speech import Speech

    if len(sys.argv) > 1:
        text=sys.argv[1]
        speech = Speech(text=text, lang='zh-CN')
        param = ("speed", "0.9")
        speech.play(param)
