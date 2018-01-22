#!/usr/bin/env python
import argparse
import datetime
from taiga import TaigaAPI

def default_doc_style():
    return """
html, body {
    max-width: 100%%;
    overflow-x: hidden;
}
body {
    font-family: arial;
    padding: 20px;
}
.epic_list {
    list-style-type: none;
    padding-left: 0;
}
.epic_item {
    page-break-after: always;
}
.epic_item > .subject {
    border: 2px solid #006699;
    color: #006699;
    text-align: center;
    font-size: 140%%;
}
.user_story_list {
    list-style-type: none;
    padding-left: 0;
}
.user_story_item > .subject {
    text-align: left;
    color: #006699;
    font-size: 140%%;
}
img {
    width: 90%%;
    text-align: center;
    padding: 20px;
}
footer {
    border-top: 1px solid gray;
    padding: 10px;
}
footer .print-date {
    float: right;
}
header {
    border-bottom: 1px solid gray;
    padding: 10px;
}
""";


def print_HTML_doc_opener(host, project):

    print("""
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <base href="{host}" target="_blank">
    <title>{title}</title>
    <style>
        {style}
    </style>
  </head>
  <body>
    <header>
        <h3 class="title">{title}</h3>
        <div class="subtitle">{subtitle}</div>
    </header>
    <article class="content">
""".format(host=host, title=project.name, subtitle=project.description, style=default_doc_style()))


def print_HTML_doc_closer(copyright):
    now = datetime.datetime.now()
    print("""
    </article>
    <footer>
        <span class="copyright">{copyright}</span>
        <span class="print-date">Printed on {print_date}</span>
    </footer>
    </body>
</html>
""".format(
    print_date=now.strftime('%Y-%m-%d %H:%M:%S'),
    copyright='&copy; Copyright %d %s' % (now.year, copyright) if copyright else ''
    ))


def dump_project_list(projects):
    print('Available Projects:')
    for project in projects:
        print('[%4d] %s "%s"' % (project.id, project.slug, project.name))


def render_item(item_class, item, extra_html='', indent=0):
    """
    Renders either a user story or epic item

    Example:
    <li class="item_class">
        <h1 class="subject">item.subject</h1>
        <p class="description">item.description</p>
        ... extra_html ...
    </li>
    """
    html = """
{indent}<li class="{item_class}">
{indent}    <h1 class="subject">{subject}</h1>
{indent}    <div class="description">{description}</div>
{indent}    {extra_html}
{indent}</li>
""".format(item_class=item_class, subject=item.subject, description=item.description_html,
    extra_html=extra_html, indent=' ' * (indent * 4))
    return html


def render_user_stories(project, epic, user_stories, summary=False):

    if summary:
        # Use CSV format instead of HTML
        text = ''
        for user_story in user_stories:
            if epic:
                text += '"%s",' % epic.subject
            text += '"%s",%d,"%s",%.1f\n' % (
                user_story.milestone_name if user_story.milestone_name is not None else '',
                user_story.ref,
                user_story.subject.replace('"', '""'),
                user_story.total_points if user_story.total_points else 0.0,
            )
        return text.strip()

    # Prepare user story list
    html = '<ul class="user_story_list">'
    for user_story in user_stories:
        item = user_story if summary else project.get_userstory_by_ref(user_story.ref)
        html += render_item("user_story_item", item, indent=3)
    html += ' ' * 8 + '</ul>'

    # if epic has been specified, wrap user story list inside an epic item
    if epic:
        item = epic if summary else project.get_epic_by_ref(epic.ref)
        html = render_item("epic_item", item, extra_html=html, indent=1)

    return html


def print_project(host, username, password, project_slug_or_name, summary, copyright):

    def find_project(project, project_slug_or_name):
        for p in projects:
            try:
                if p.slug == project_slug_or_name or p.name == project_slug_or_name:
                    return p
                if p.id == int(project_slug_or_name):
                    return p
            except:
                pass
        return None

    api = TaigaAPI(host=host)
    api.auth(username=username, password=password)

    projects = api.projects.list()
    if not project_slug_or_name:
        dump_project_list(projects)
    else:

        project = find_project(projects, project_slug_or_name)
        if project is None:
            print('Project "%s" not found' % project_slug_or_name)
        else:

            epics = project.list_epics()

            if not summary:
                print_HTML_doc_opener(host, project)
            else:
                header = '' if len(epics) <= 0 else "Epic;"
                header += 'Milestone;Ref;User_story;Points'
                print(header)

            if len(epics) <= 0:
                user_stories = project.list_user_stories()
                print(render_user_stories(project, None, user_stories, summary=summary))
            else:
                if not summary: print('<ul class="epic_list">')
                for epic in epics:
                    user_stories = epic.list_user_stories(pagination=False, order_by="epic_order")
                    print(render_user_stories(project, epic, user_stories, summary=summary))
                if not summary: print('</ul>')

            if not summary:
                print_HTML_doc_closer(copyright)


def main():

    # See: https://docs.python.org/2/library/argparse.html
    parser = argparse.ArgumentParser(description='Extract printable report from Taiga Project')
    parser.add_argument('host', help="remote host")
    parser.add_argument('username')
    parser.add_argument('password')
    parser.add_argument('--project', default='')
    parser.add_argument('--copyright', '-c', default='')
    parser.add_argument('--summary', '-s', action='store_true')
    args = parser.parse_args()

    print_project(args.host, args.username, args.password, args.project, args.summary, args.copyright)

if __name__ == "__main__":
    main()
