import os
import sys

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(DIR, 'deps'))

import djangogo

parser = djangogo.make_parser()
args = parser.parse_args()
djangogo.main(args,
    project='datasaver_proj',
    app='datasaver',
    db_name='datasaver_database',
    db_user='datasaver_user',
    heroku_url='https://dans-datasaver.herokuapp.com/',
)
