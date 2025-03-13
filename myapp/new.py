from django.template.loader import get_template
get_template("blog/index.html")  # ✅ Should NOT give an error
