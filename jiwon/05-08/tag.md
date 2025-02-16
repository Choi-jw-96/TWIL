# 1. 오픈소스 다운
```bash
# tag를 도와주는 패키지
pip install django-taggit
# tag의 활용을 도와주는 패키지
pip install django-taggit-templatetags2
```

# 2. settings.py + taggit 설정

```py
INSTALLED_APPS = [
	...
	'taggit.apps.TaggitAppConfig',
    'taggit_templatetags2',
    ...
]


# 대소문자 처리
TAGGIT_CASE_INSENSITIVE = True

# 태그 클라우드에서 표시할 최대 태그 수
TAGGIT_LIMIT = 50

# 태그 최대 길이(기본 50)
TAGGIT_MAX_TAG_LENGT = 30

# 빈 태그 생성을 막는다
TAGGIT_REMOVE_EMPTY = True

# 문자열에서 태그 추출 구분자(기본',')
TAGGIT_TAGS_FROM_STRING = ''

# 모델에서 태그 추출 구분자(기본',')
TAGGIT_TAGS_FROM_MODEL = ''

# 중복 태그를 허용하는가 (기본 False)
TAGGIT_ALLOW_DUPLICATES = False
```
[taggit](https://django-taggit.readthedocs.io/en/latest/)


# 3. models.py에 적용
```py
from taggit.managers import TaggableManager
from django.urls import reverse

class Article(models.Model):
    # 태그를 넣어준다
    tags = TaggableManager(blank=True)
    
    # tag를 쓴 detail에 연결이 편하기 위해 위해사용
	def get_absolute_url(self):
        return reverse('articles:detail', args=[int(self.id)])
```

# 4. admin.py
```py
    list_display = ('title', 'content', 'tag_list',)
    list_filter = ('tag_list',)
    # 검색 박스 표시, title, content 칼럼에서 검색
    search_fields = ('title', 'content')
    # title 필드를 사용해 미리 채워지도록
    prepopulated_fields = {'slug':('title',)}
	
    # Article 레코드 리스트를 가져오는 메소드 오버라이딩
    # N:N 관계에서 쿼리 횟수를 줄여 성능 높일때 : prefetch_related
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')
    
    def tag_list(self, obj):
        return ', '.join(o.name for o in obj.tags.all())
```

# 5. forms.py
```py
class ArticleForm(forms.ModelForm):
    tags = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder' : '태그 사이에 쉼표를 넣어주세요.'
            }
        )
    )

    class Meta:
        model = Article
        fields = ('tags')
```

# 6. views.py
```py
@login_required
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        # 태그를 , 기준으로 분리
        tags = request.POST.get('tags').split(',')
        if form.is_valid():
            article.save()
            # tags를 하나씩 article.tags에 넣어준다
            for tag in tags:
                article.tags.add(tag.strip())
            return redirect('articles:index')       
    else:
        form = ArticleForm()
    context = {
        'form': form,

    }
    return render(request, 'articles/create.html', context)
```

## Update
views.py
```py
@login_required
def update(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if request.user == article.user:
        if request.method == 'POST':
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid(): 
                form.save()
                # 태그 부분을 비워준다
                article.tags.clear()
                # 초기태그를 ','씩 분리하여 다시 불러온다
                tags = request.POST.get('tags').split(',')
                # 태그를 하나씩 tags에 넣어준다.
                for tag in tags:
                    article.tags.add(tag.strip())
            
        else:
        	# 초기 태그를 불러온다(해당 article의 모든태그의 값을 ', '사이에 넣어서 불러온다
            initial_tags = ', '.join(article.tags.all().values_list('name', flat=True))
            form = ArticleForm(instance=article, initial={'tags': initial_tags})

    context = {
        'form': form,
        'article': article,
    }
    return render(request, 'articles/update.html', context)
```

