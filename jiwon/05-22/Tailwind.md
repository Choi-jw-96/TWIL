# Tailwind CSS
- Utility-First : 미리 세팅된 유틸리티 클래스를 활용하여 HTML 코드 내에서 스타일링
== bootstrap

## 장점 :
- 커스터마이징 가능 : 기본 정의된 테마를 확장 / 새로운 속성 정의 가능
- 반복되는 클래스 추사화
- 다크모드 지원 (dark:)
- 배포 시 사용하지 않는 유틸리티 스타일 시트를 제거하는 purge 옵션 존재

## 단점
- 가시성이 떨어짐

```
<div class="bg-slate-100 rounded-xl p-8 dark:bg-slate-800">
```

- 우선순위 : 뒤에 위치한 클래스를 최종적으로 적용
- 특정 css 지원 불가 : hover: 혹은 focus: 등 특정 프리픽스는 일부 속성만 사용가능(커스터마이징을 통해 추가 설정을 넣어주면 제공됨)
- 다른 css 프레임워크처럼 완성된 스타일을 제공하지 않는다

### tip 
Tailwind CSS IntelliSense 플러그인 추천(vscord)
- 자동완성 기능


## 사용법
- CDN 불러오기
```html
<script src="https://cdn.tailwindcss.com"></script>
```

- tailwind.config라는 전역 속성에 단순히 설정 객체를 할당
tailwind.config.js 설정없이 사용
```css
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            tomato: "tomato",
          },
        },
      },
    };
<!-- 토마토 색을 적용 -->
```

- 추가로 정의가 필요한 클래스가 있다면  CSS 코드를 작성하듯이 @layer 지시문을 사용하여 클래스를 추가
```
    @layer components {
      .btn {
        @apply rounded bg-blue-500 px-4 py-2 font-bold text-white hover:bg-blue-600;
      }
    }
```
체험 등 견본을 볼 수 있다
[tailwindplay](https://play.tailwindcss.com/)



## @layer
그룹화 & 우선순위를 정하기
- 레이어는 선언 순서에 따라 스타일이 적용되며, 늦게 선언될수록 높은 우선순위를 갖는다
-  순서를 미리 정의하는것도 가능하다
```css
@layer layer_1 {
  .text {
    color: red;
    font-weight: 700;
  }
}

@layer layer_2 {
  .text {
    color: blue;
  }
}

@layer layer_3 {
  .text {
    color: orange;
    font-weight: 400;
  }
}
```
-> 3, 2, 1

```css
@layer layer_3, layer_1, layer_2
```
추가시 2, 1, 3


- 이름 재사용가능 (같은 이름 시 위에 추가된다는 개념)
- 익명 / url로 외부스타일의 레이어 생성가능
```css
@layer { ... }

@import url(basic.css) layer;
```

- revert-layer로 이전 레이어 스타일 적용
- @layer로 선언치 않은 스타일은 높은 우선순위를 가진다.
- 레이어 끼리 되어있는 것은 우선순위에서 선택자 명시도는 무의미
---






## Crispy-Tailwind
: Tailwind CSS를 기반으로 한 Python 라이브러리
 Django-Crispy-Forms과 같이 템플릿 태그를 사용하여 스타일을 적용

1. Crispy-Tailwind를 설치
```bash
pip install crispy-tailwind
```

2. Django 설정
```py
INSTALLED_APPS = [
    # ...
    'crispy_tailwind',
    'crispy_forms',
    # ...
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"
```

3. Tailwind CSS 적용
Tailwind CSS 스타일을 적용하기 위해 Django 템플릿에서 Crispy-Tailwind 태그를 사용
폼을 렌더링하는 템플릿 파일을 열고, 다음과 같이 Crispy-Tailwind 태그를 추가
```py
# forms.py
from django import forms
from crispy_tailwind.forms import TailwindFormMixin

class MyForm(TailwindFormMixin, forms.Form):
    name = forms.CharField(label="Name")
    email = forms.EmailField(label="Email")
    message = forms.CharField(label="Message", widget=forms.Textarea)
```
```html
{% load crispy_tailwind_tags %}

<form method="post" class="crispy tailwind">
    {% csrf_token %}
    {{ form|crispy }}
</form>
```


5. Collect static
Tailwind CSS 스타일 시트를 수집하기 위해 정적 파일을 수집해야 합니다. 
```
python manage.py collectstatic
```