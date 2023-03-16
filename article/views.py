from openpyxl.reader.excel import load_workbook
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from article.serializers import RequestSerializer
from article.services import get_product_data_list


class ArticleView(viewsets.GenericViewSet):

    @action(detail=False, methods=['POST'], serializer_class=RequestSerializer, url_path='code')
    def article_code(self, request):
        serializer = RequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data.get('file'):
            # Read xlsx file
            wb = load_workbook(serializer.validated_data['file'])
            sheet = wb.active
            rows = sheet.rows
            article_list = [str(int(row[0].value)) for row in rows]
            res = get_product_data_list(article_list)
            print(res)
            return Response(res.dict(), status=200)

        elif serializer.validated_data.get('article'):
            # Send request from string
            article = serializer.validated_data['article']
            res = get_product_data_list(article)
            return Response(res.dict(), status=200)

        else:
            return Response({"error": "No input provided."}, status=400)

