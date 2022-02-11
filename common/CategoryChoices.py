class CategoryChoices:

    CATEGORY_CHOICES = [
        ('Painting', 'Painting'),
        ('Container', 'Container'),
        ('Drawing', 'Drawing'),
        ('Photography', 'Photography'),
        ('Sketch Pad', 'Sketch Pad'),
        ('Electromedia', 'Electromedia'),
        ('Videograms', 'Videograms'),
        ('Poetry Poster', 'Poetry Poster'),
        ('Notebook', 'Notebook'),
        ('Album', 'Album'),
    ]

    @staticmethod
    def category_choices():
        return CategoryChoices.CATEGORY_CHOICES

    @staticmethod
    def gen_suffix(category):
        if category == 'Painting':
            suffix = 'P'
        elif category == 'Container':
            suffix = 'B'
        elif category == 'Drawing':
            suffix = 'D'
        elif category == 'Photography':
            suffix = 'PH'
        elif category == 'Sketch Pad':
            suffix = 'P'
        elif category == 'Electromedia':
            suffix = 'E'
        elif category == 'Videograms':
            suffix = 'V'
        elif category == 'Poetry Poster':
            suffix = 'PP'
        elif category == 'Notebook':
            suffix = 'N'
        elif category == 'Album':
            suffix = 'A'
        else:
            raise ValueError(f'Unexpected category {category}')
        return suffix

    @staticmethod
    def decode_item_id(item_id):
        if item_id.startswith('AT.PP'):
            category = 'Poetry Poster'
        elif item_id.startswith('AT.D'):
            category = 'Drawing'
        elif item_id.startswith('AT.P'):
            category = 'Painting'
        elif item_id.startswith('AT.E'):
            category = 'Electromedia'
        elif item_id.startswith('AT.B'):
            category = 'Container'
        else:
            raise ValueError(f'Unexpected item_id {item_id}')
        return category
