from application import application
import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    application.run(debug=True,host='127.0.0.1',port=port)
