def count_user_clicks_middleware(get_response):
    def middleware(request):
        clicks_count = request.session.get('clicks_count', )
        clicks_count +=1
        request.session['clicks_count']= clicks_count
        request.clicks_count = clicks_count
        return get_response(request)
    return middleware