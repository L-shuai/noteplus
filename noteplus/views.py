from django.shortcuts import render


def bad_request(request, exception, template_name='error/400.html'):
	return render(request, template_name)


def permission_denied(request, exception, template_name='error/403.html'):
	return render(request, template_name)


def page_not_found(request, exception, template_name='error/404.html'):
	return render(request, template_name)


def server_error(request, template_name='error/500.html'):
	return render(request, template_name)


# def page_not_found(request, exception):
# 	# 404
# 	return render(request, "error/404.html", status=404)
#
#
# def page_error(exception):
# 	return render("error/500.html", status=500)
#
#
# def permission_denied(request, exception):
# 	# 403
# 	return render(request, "error/403.html", status=403)
#
#
# def bad_request(request, exception):
# 	# 400
# 	return render(request, "error/400.html", status=400)