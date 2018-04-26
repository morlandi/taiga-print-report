import datetime
from taiga import TaigaAPI
from taiga.models import Milestone


def default_doc_style():
    return """
html, body {
    max-width: 100%;
    overflow-x: hidden;
}
body {
    font-family: arial;
    padding: 20px;
}
.project-title {
    color: #006699;
}
.wiki_page_list {
    list-style-type: none;
    padding-left: 0;
}
.section_list {
    list-style-type: none;
    padding-left: 0;
}
.section_item {
    page-break-after: always;
}
.section_item > .subject {
    border: 2px solid #006699;
    color: #006699;
    text-align: center;
    font-size: 140%;
}
.user_story_list {
    list-style-type: none;
    padding-left: 0;
}
.user_story_item > .subject {
    text-align: left;
    color: #006699;
    font-size: 140%;
}
img {
    width: 90%;
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
.discreet {
    color: #aaa;
    font-size: 14px;
    font-weight: normal;
}
table {
    border-collapse: collapse;
}
table th,
table td {
    border: 1px solid #999;
    padding: 2px;
}
.wiki_page_item {
    page-break-after: always;
}
.wiki_page_item .description h1 {
    color: #006699;
}
.tasks_table {
    width: 90%;
    margin: 0 auto;
    border-collapse: collapse;
    table-layout: fixed;
}
.tasks_table td,
.tasks_table th {
    padding: 6px 16px;
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
        <h1 class="project-title">{title}</h1>
        <div class="project-subtitle">{subtitle}</div>
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
    if isinstance(item, Milestone):
        html = """
{indent}<li class="{item_class}">
{indent}    <h1 class="subject">{subject}</h1>
{indent}    <div class="description">{description}</div>
{indent}    {extra_html}
{indent}</li>
""".format(item_class=item_class, subject=item.name, description='',
    extra_html=extra_html, indent=' ' * (indent * 4))
    else:
        html = """
{indent}<li class="{item_class}">
{indent}    <h1 class="subject">{subject} <span class="discreet">(#{ref})</span></h1>
{indent}    <div class="description">{description}</div>
{indent}    {extra_html}
{indent}</li>
""".format(item_class=item_class, subject=item.subject, ref=item.ref, description=item.description_html,
    extra_html=extra_html, indent=' ' * (indent * 4))

    return html


def render_tasks(project, tasks, task_headers):
    html = ''
    if len(tasks):
        html = '<table class="tasks_table">'
        if task_headers:
            html += '<thead><tr>' + ''.join(['<th>%s</th>' % th for th in task_headers]) + '</tr></thead>'
        html += '<tbody>'
        for row in tasks:
            task = project.get_task_by_ref(row.ref)
            html += '<tr><td>{name} <span class="discreet">(#{ref})</span></td><td>{description}</td></tr>'.format(
                ref=task.ref, name=task.subject, description=task.description_html,
            )
        html += '</tbody></table>'
    return html


def render_user_stories(project, epic, user_stories, summary=False, include_tasks=False, task_headers=[]):

    if summary:
        # Use CSV format instead of HTML
        text = ''
        for user_story in user_stories:
            if epic:
                text += '"%s";' % str(epic)
            text += '"%s";%d;"%s";%.1f\n' % (
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

        html_tasks = ''
        if include_tasks:
            tasks = item.list_tasks()
            html_tasks = render_tasks(project, tasks, task_headers)

        html += render_item("user_story_item", item, extra_html=html_tasks, indent=3)

    html += ' ' * 8 + '</ul>'

    # if epic has been specified, wrap user story list inside an epic item
    if epic:
        #item = epic if summary else project.get_epic_by_ref(epic.ref)
        try:
            item = project.get_epic_by_ref(epic.ref)
        except:
            item = epic
        html = render_item("section_item", item, extra_html=html, indent=1)

    return html


def render_wiki_pages(project):
    html = ''
    wiki_pages = project.list_wikipages()
    if len(wiki_pages) > 0:
        indent = 1
        html = '<ul class="wiki_page_list">'
        for wiki_page in wiki_pages:
            html += """
{indent}<li class="wiki_page_item">
{indent}    <div class="description">{description}</div>
{indent}</li>
""".format(description=wiki_page.html, indent=' ' * (indent * 4))
        html += ' ' * 8 + '</ul>'
    return html


def print_project(host, username, password, project_slug_or_name, summary,
    print_wiki_pages, copyright, group_by_epics, include_tasks, task_headers):

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

    def filter_user_stories(user_stories, ref):
        if ref is not None:
            user_stories = [u.ref for u in user_stories if u.ref==ref]
        return user_stories

    api = TaigaAPI(host=host)
    api.auth(username=username, password=password)

    projects = api.projects.list()
    if not project_slug_or_name:
        dump_project_list(projects)
    else:

        project = find_project(projects, project_slug_or_name)
        if project is None:
            print('Project "%s" not found' % project_slug_or_name)
        elif print_wiki_pages:
            print_HTML_doc_opener(host, project)
            print(render_wiki_pages(project))
            print_HTML_doc_closer(copyright)
        else:

            if not summary:
                print_HTML_doc_opener(host, project)
            else:
                #header = '' if len(epics) <= 0 else "Epic;"
                header = 'Epic;Milestone;Ref;User_story;Points'
                print(header)

            # List Sections (either Milestones or Epics)
            sections = None
            if group_by_epics:
                sections = project.list_epics()
            else:
                try:
                    sections = project.list_milestones(order_by="estimated_start")
                except Exception as e:
                    print(e)
                    import ipdb; ipdb.set_trace()

            if len(sections) <= 0:
                # List all user stories
                user_stories = project.list_user_stories()
                print(render_user_stories(project, None, user_stories, summary=summary,
                    include_tasks=include_tasks, task_headers=task_headers))
            else:
                # Navigate sections
                if not summary: print('<ul class="section_list">')
                for section in sections:
                    try:
                        user_stories = [us for us in section.user_stories]
                        # Try to sort by sprint order
                        try:
                            user_stories = sorted(user_stories, key=lambda x: x.sprint_order)
                        except:
                            pass
                    except AttributeError:
                        user_stories = section.list_user_stories(pagination=False, order_by="epic_order")
                    print(render_user_stories(project, section, user_stories, summary=summary,
                        include_tasks=include_tasks, task_headers=task_headers))
                if not summary: print('</ul>')

            if not summary:
                print_HTML_doc_closer(copyright)
