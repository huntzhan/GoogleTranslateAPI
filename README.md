# Motivation

After released [mgd v0.1](https://github.com/haoxun/MyGoogleDict)(a command-line front end of google translation service), I realized that there's few mature python package could fulfill my requirements, such as fine-grained single word translation and TTS service. This project is proposed for providing an end solution of google translation api.

This project is mainly inspired by [goslate](https://bitbucket.org/zhuoqiang/goslate) and [Google-Translate-TTS](https://github.com/hungtruong/Google-Translate-TTS/).


# Interface
* TranslateService.trans_details(self, src_lang, tgt_lang, src_text)
* TranslateService.trans_sentence(self, src_lang, tgt_lang, src_text)
* TranslateService.detect(self, src_text)
* TTSService.get_mpeg_binary(self, tgt_lang, src_text)

Interfaces presented above is quite self-explaining. For more information, such as please read documentation strings of each interface.

# Example of Usage
## TranslateService

	Python 3.3.3 (default, Dec 10 2013, 18:43:00)
	[GCC 4.2.1 Compatible Apple LLVM 5.0 (clang-500.2.79)] on darwin
	Type "help", "copyright", "credits" or "license" for more information.
	>>> import google_translate_api as api
	>>> translator = api.TranslateService()
	>>> translator.trans_details('en', 'zh-CN', 'test')
	{'sentences': [{'orig': 'test', 'trans': '测试', 'src_translit': '', 'translit': 'Cèshì'}], 'dict': [{'pos': 'noun', 'entry': [{'reverse_translation': ['test', 'examination'], 'score': 0.61608213, 'word': '测试'}, {'reverse_translation': ['test', 'experiment', 'tentative'], 'score': 0.18211353, 'word': '试验'}, {'reverse_translation': ['test', 'examination', 'experiment', 'exam', 'fitting'], 'score': 0.019194625, 'word': '试'}, {'reverse_translation': ['experiment', 'test'], 'score': 0.013611027, 'word': '实验'}, {'reverse_translation': ['examination', 'exam', 'test'], 'score': 0.012588142, 'word': '考试'}, {'reverse_translation': ['test', 'trial', 'ordeal'], 'score': 0.012392981, 'word': '考验'}, {'reverse_translation': ['test', 'quiz'], 'score': 0.0078774579, 'word': '测验'}], 'base_form': 'test', 'terms': ['测试', '试验', '试', '实验', '考试', '考验', '测验'], 'pos_enum': 1}, {'pos': 'verb', 'entry': [{'reverse_translation': ['test', 'examine', 'inspect'], 'score': 0.043255754, 'word': '检验'}, {'reverse_translation': ['test', 'try'], 'score': 0.019194625, 'word': '试'}, {'reverse_translation': ['test', 'study', 'examine', 'investigate', 'verify', 'check'], 'score': 0.011461634, 'word': '考'}, {'reverse_translation': ['test', 'put to test'], 'score': 0.0078774579, 'word': '测验'}, {'reverse_translation': ['test', 'check', 'verify', 'examine', 'prove', 'confirm'], 'score': 0.0011893183, 'word': '验'}, {'reverse_translation': ['test', 'investigate', 'check', 'study'], 'score': 0.00041749, 'word': '考查'}, {'reverse_translation': ['taste', 'flavor', 'try the flavor', 'test', 'flavour'], 'score': 7.5711552e-07, 'word': '尝'}], 'base_form': 'test', 'terms': ['检验', '试', '考', '测验', '验', '考查', '尝'], 'pos_enum': 2}], 'src': {'en': 1.0}, 'server_time': 4, 'spell': {'spell_res': 'Test', 'related': True, 'correction_type': [10]}}
	>>> translator.trans_sentence('en', 'zh-CN', 'test')
	'测试'
	>>> translator.detect('test')
	{'en': 1.0}
	
## TTSService

	>>> tts = api.TTSService()
	>>> import subprocess
	>>> import tempfile
	>>> with tempfile.NamedTemporaryFile() as f:
	...     data = tts.get_mpeg_binary('en', 'This is a sentence.')
	...     f.write(data)
	...     subprocess.call(['afplay', f.name])

