import os

BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'app.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = b'\xec\x14\x00\xe9\xc6FH\xf7\xf6\xe3\x06\xb0l.\xb9z'

JWT_SECRET_KEY = '11646675a12ce4acb4f79e6a4851c24e56f69510564378aa36249e0ddcd7d083a323f7045c39e0b338303bfbe16f4b8763cd53fab48d9ae887d9c17f5948bb54051706dbbeb2efb92b2bb847b095da9ad07761eb138ceaa47657c4a4e5f5bc3044384467fd01433a9ba322525a9a853c2da3856c17e324a6ce692384f313007379200cd5ba77d197322bc38fc8e0b5f424a73e490f79b4e4208e1d9da3523741aa473a2a8dd408544e972757705370baffbfddfd61624a7a586a24c61200656f8977c965ce3c651fe78f5730b3400064ebebcd1ca146424a736372aaedca94e4feb0eaeba5a960cf1184446a77ddb3a3dee9631430274d5ede3c3ec1b7d5235c'
