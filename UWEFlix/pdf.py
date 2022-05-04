from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse

#
def getStatementPDF(template, context):
    #
    template = get_template(template)
    #
    statement_html = template.render(context)
    #
    data = BytesIO()
    #
    pdf = pisa.pisaDocument(BytesIO(statement_html.encode("ISO-8859-1")), data)
    #
    return HttpResponse(data.getvalue(), content_type='application/pdf')