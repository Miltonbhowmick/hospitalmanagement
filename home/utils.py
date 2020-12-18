from django.utils.text import slugify

def _get_unique_slug(slug_field, model):

	if slug_field:
		slug_field_lenght = len(slug_field)

		slug_field = slug_field[:50] if slug_field_lenght>50 else slug_field

		slug = slugify(slug_field, allow_unicode=True)
		unique_slug = slug
		num=1
		while model.objects.filter(slug = unique_slug).exists():
			unique_slug = '{}-{}'.format(slug,num)
			num+=1
		return unique_slug