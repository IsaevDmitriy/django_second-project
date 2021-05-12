from collections import Counter

from django.shortcuts import render

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    result = request.GET.get('from-landing', None)
    counter_click[result] += 1
    print(f'Количество переходов - {counter_click.most_common()}')
    return render(request, 'index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    data = {
        "original": 'landing.html',
        "test": 'landing_alternate.html'
    }
    lan = request.GET.get('ab-test-arg', None)
    if lan == None:
        lan = "original"
    counter_show[lan] += 1
    print(f'Количество показов - {counter_show.most_common()}')
    result = data[lan]
    return render(request, result)


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Для вывода результат передайте в следующем формате:
    if counter_show['original'] != 0 and counter_click['original'] != 0:
        original_conversion = counter_click['original'] / counter_show['original']
    else:
        original_conversion = 0
    if counter_show['test'] != 0 and counter_click['test'] != 0:
        test_conversion = counter_click['test']/counter_show['test']
    else:
        test_conversion = 0
    return render(request, 'stats.html', context={
        'test_conversion': test_conversion,
        'original_conversion': original_conversion,
    })

