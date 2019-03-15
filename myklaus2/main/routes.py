from flask import Blueprint, render_template, request

main = Blueprint("main", __name__)

#Nur ein Platzhalter sobald die Dokumente aus der DB gezogen werden kommt das weg
class Documents():
    items = [
        {
            'course': {
                'faculty': {
                    'name': 'E und I'
                },
                'name': 'Mathe 1'
            },
            'type': 'Klausur',
            'docent': 'Vogt',
            'semester': 'WS18/19',
        },
        {
            'course': {
                'faculty': {
                    'name': 'E und I'
                },
                'name': 'Programmieren 2'
            },
            'type': 'Klausur',
            'docent': 'Kratzke',
            'semester': 'SS18',
        },
        {
            'course': {
                'faculty': {
                    'name': 'E und I'
                },
                'name': 'Programmieren 2'
            },
            'type': 'Lösungen',
            'docent': 'Kratzke',
            'semester': 'SS18',
        }
    ]

    page = 1
    pages = 11
    
    def iter_pages(self, left_edge=2, right_edge=2, left_current=2, right_current=3):
        return iter([1,2,None,4,5,6,7,8,None,10,11])

@main.route("/")
def home():
    page = request.args.get('p', 1, type=int)
    search = request.args.get('s', '')
    field = request.args.get('f', 0, type=int)
    documents = Documents()
    documents.page = page
    #documents = Documents.query.filter(reques).order_by().paginate(page=page, per_page=25)
    return render_template("home.html", documents=documents, s=search, f=field)