from typing import Callable, Type
from urllib.parse import parse_qs

from app.router import Router
from app.services import MatchesCacheService, ScoreboardService, DatabaseService
from app.views import BaseView, ViewToHTML
from app.exceptions import (
    MethodNotAllowed, PathNotFoundError, MissingRequestHeadersError, MissingRequestFieldsError,
    MatchNotFoundError, InvalidUsernameError
)


def parse_request_body(environ: dict):
    try:
        content_length = int(environ.get('CONTENT_LENGTH', 0))
    except ValueError:
        content_length = 0

    if content_length > 0:
        body = environ['wsgi.input'].read(content_length).decode('utf-8')
        return {key: value[0] for key, value in parse_qs(body).items()}

    return {}


def parse_request_params(environ: dict):
    query_string = environ['QUERY_STRING']

    if query_string:
        return {key: value[0] for key, value in parse_qs(query_string).items()}

    return {}


@Router.route(path='/', method='GET')
def index_get_handler(environ, start_response: Callable, view: Type["BaseView"] = ViewToHTML):
    html = view.render_template(template_name='index.html')

    start_response('200 OK', [('Content-Type', 'text/html')])

    return [html.encode('utf-8')]


@Router.route(path='/new-match', method='GET')
def new_match_get_handler(environ, start_response: Callable, view: Type["BaseView"] = ViewToHTML):
    html = view.render_template(template_name='new-match.html')

    start_response('200 OK', [('Content-Type', 'text/html')])

    return [html.encode('utf-8')]


@Router.route(path='/match-score', method='GET')
def match_score_get_handler(environ, start_response: Callable, view: Type["BaseView"] = ViewToHTML):
    try:
        uuid = parse_request_params(environ)['uuid']
    except KeyError:
        raise MissingRequestHeadersError('uuid', )

    match = DatabaseService.get_match_by_uuid_with_players(uuid=uuid)

    html = view.render_template(
        template_name='match-score.html',
        match=match
    )

    start_response('200 OK', [('Content-Type', 'text/html')])

    return [html.encode('utf-8')]


@Router.route(path='/matches', method='GET')
def matches_get_handler(environ, start_response: Callable, view: Type["BaseView"] = ViewToHTML):
    MATCHES_PER_PAGE = 10

    data = parse_request_params(environ)
    page, player_name = int(data.get('page', 1)), data.get('filter_by_player_name')

    total_pages = MatchesCacheService.get_cached_data(player_name)

    if total_pages is None:
        matches = DatabaseService.get_matches_list(filter_by_player_name=player_name)
        total_pages = MatchesCacheService.calculate_total_pages(total_matches=len(matches))

        MatchesCacheService.cache_data(
            player_name=player_name,
            total_pages=total_pages
        )

    players = DatabaseService.get_players_list()
    matches = DatabaseService.get_matches_list(
        filter_by_player_name=player_name,
        offset=(page-1) * MATCHES_PER_PAGE,
        count=MATCHES_PER_PAGE
    )

    html = view.render_template(
        template_name='matches.html',
        matches=matches,
        players=players,
        filter_by_player_name=player_name,
        total_pages=total_pages,
        page=page
    )

    start_response('200 OK', [('Content-Type', 'text/html')])

    return [html.encode('utf-8')]


@Router.route(path='/new-match', method='POST')
def new_match_post_handler(environ, start_response: Callable, view: Type["BaseView"] = ViewToHTML):
    data = parse_request_body(environ)

    try:
        first_player_name, second_player_name = data['player1'], data['player2']
    except KeyError:
        raise MissingRequestHeadersError('player1', 'player2')

    uuid = DatabaseService.add_match(
        first_player_name=first_player_name, second_player_name=second_player_name
    ).uuid

    MatchesCacheService.invalidate_cache()

    start_response('302 Found', [('Location', f'/match-score?uuid={uuid}')])

    return []


@Router.route(path='/match-score', method='POST')
def match_score_post_handler(environ, start_response: Callable, view: Type["BaseView"] = ViewToHTML):
    try:
        uuid = parse_request_params(environ)['uuid']
    except KeyError:
        raise MissingRequestHeadersError('uuid', )

    try:
        winner = parse_request_body(environ)['winner']
    except KeyError:
        raise MissingRequestFieldsError('winner', )

    score = ScoreboardService.update_match_score(
        score=DatabaseService.get_match_by_uuid_with_players(uuid=uuid).score,
        winner_name=winner
    )

    DatabaseService.update_match_score_by_uuid(
        uuid=uuid,
        score=score
    )

    if ScoreboardService.is_win(score=score):
        DatabaseService.update_match_winner_by_uuid(
            uuid=uuid,
            winner_name=winner
        )

    start_response('302 Found', [('Location', f'/match-score?uuid={uuid}')])

    return []


@Router.route(path='/exception', method='GET')
def exception_handler(environ, start_response: Callable, view: Type["BaseView"] = ViewToHTML):
    ERROR_CODES = {
        PathNotFoundError: '404 Not Found',
        MethodNotAllowed: '405 Method Not Allowed',
        MissingRequestHeadersError: '400 Bad Request',
        MissingRequestFieldsError: '400 Bad Request',
        MatchNotFoundError: '404 Not Found',
        InvalidUsernameError: '422 Unprocessable Entity',
        Exception: '500 Internal Server Error'
    }

    exception = environ.get('exception')

    if exception:
        status = ERROR_CODES.get(type(exception))
        start_response(status, [('Content-Type', 'text/html')])
        html = view.render_template('exception.html', exception=str(exception))
        return [html.encode('utf-8')]
    else:
        status = '500 Internal Server Error'
        start_response(status, [('Content-Type', 'text/html')])
        html = view.render_template('exception.html', exception='Unknown error')
        return [html.encode('utf-8')]
