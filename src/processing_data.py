import cgi
import io


def extract_form_data(event):
    fp = io.BytesIO(event["body"].encode("utf-8"))
    pdict = cgi.parse_header(event["headers"]["Content-Type"])[1]

    if "boundary" in pdict:
        pdict["boundary"] = pdict["boundary"].encode("utf-8")

    pdict["CONTENT-LENGTH"] = len(event["body"])
    form_data = cgi.parse_multipart(fp, pdict)

    # Concate string in params
    for key, value in form_data.items():
        form_data[key] = " ".join(value)

    return form_data