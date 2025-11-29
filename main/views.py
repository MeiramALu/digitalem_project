import asyncio
import telegram
from django.shortcuts import render, get_object_or_404
from .models import TeamMember, Project, News, Service
from django.http import JsonResponse
from django.conf import settings


def index(request):
    team_members = TeamMember.objects.filter(is_visible=True)[:6]
    latest_news = News.objects.all()[:3]
    services = Service.objects.all()[:4]
    context = {
        'team': team_members,
        'latest_news': latest_news,
        'services': services,
    }
    return render(request, 'main/index.html', context)


def team_list(request):
    all_team_members = TeamMember.objects.filter(is_visible=True)
    context = {
        'all_team': all_team_members
    }
    return render(request, 'main/team_list.html', context)


def labs(request):
    return render(request, 'main/labs.html')


def project_list(request, category_slug):
    category_map = {
        'research': 'Научные исследования',
        'development': 'Проекты в разработке',
        'commercial': 'Коммерциализация'
    }
    category_name = category_map.get(category_slug, 'Проекты')
    projects = Project.objects.filter(category=category_slug)
    context = {
        'projects': projects,
        'category_name': category_name
    }
    return render(request, 'main/project_list.html', context)


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)

    team_members = project.team.filter(is_visible=True)

    keywords_list = []
    if project.keywords:
        keywords_list = [keyword.strip() for keyword in project.keywords.split(',')]
    context = {
        'project': project,
        'team_members': team_members,
        'keywords_list': keywords_list
    }
    return render(request, 'main/project_detail.html', context)


def team_member_detail(request, slug):
    member = get_object_or_404(TeamMember, slug=slug)
    projects = member.projects.all()
    context = {
        'member': member,
        'projects': projects
    }
    return render(request, 'main/team_member_detail.html', context)


def news_list(request):
    all_news = News.objects.all()
    context = {
        'all_news': all_news,
    }
    return render(request, 'main/news_list.html', context)


def news_detail(request, slug):
    news_item = get_object_or_404(News, slug=slug)
    keywords_list = []
    if news_item.keywords:
        keywords_list = [keyword.strip() for keyword in news_item.keywords.split(',')]
    context = {
        'news_item': news_item,
        'keywords_list': keywords_list
    }
    return render(request, 'main/news_detail.html', context)


def send_telegram_message(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message_body = request.POST.get('message')

        if not all([name, phone, email, message_body]):
            return JsonResponse({'success': False, 'error': 'Все поля обязательны для заполнения.'})

        token = settings.TELEGRAM_BOT_TOKEN
        chat_id = settings.TELEGRAM_CHAT_ID

        text = (
            f"<b>Новая заявка с сайта!</b>\n\n"
            f"<b>Имя:</b> {name}\n"
            f"<b>Телефон:</b> {phone}\n"
            f"<b>Email:</b> {email}\n\n"
            f"<b>Сообщение:</b>\n{message_body}"
        )

        async def send():
            try:
                bot = telegram.Bot(token=token)
                await bot.send_message(
                    chat_id=chat_id,
                    text=text,
                    parse_mode='HTML'
                )
                return JsonResponse({'success': True})
            except telegram.error.TelegramError as e:
                return JsonResponse({'success': False, 'error': f'Ошибка Telegram: {e.message}'})

        return asyncio.run(send())

    return JsonResponse({'success': False, 'error': 'Неверный метод запроса.'})