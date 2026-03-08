from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, SubmitField
from wtforms.validators import Optional
from wtforms.widgets import ListWidget, CheckboxInput

class DownloadSearchForm(FlaskForm):
    """
    Form for filtering and searching datasets
    """

    # 关键词搜索（Study ID / Sample Name）
    keyword = StringField(
        'Keyword',
        validators=[Optional()]
    )

    # 单选过滤：Biome
    biome = SelectField(
        'Biome',
        choices=[
            ('', 'All'),
            ('gut', 'Gut'),
            ('soil', 'Soil'),
            ('ocean', 'Ocean')
        ],
        validators=[Optional()]
    )

    # 单选过滤：Data Type
    data_type = SelectField(
        'Data Type',
        choices=[
            ('', 'All'),
            ('16s', '16S rRNA'),
            ('shotgun', 'Shotgun')
        ],
        validators=[Optional()]
    )

    # 多选标签过滤
    tags = SelectMultipleField(
        'Tags',
        choices=[
            ('human', 'Human'),
            ('microbiome', 'Microbiome'),
            ('environment', 'Environment')
        ],
        option_widget=CheckboxInput(),
        widget=ListWidget(prefix_label=False),
        validators=[Optional()]
    )

    # 排序方式
    sort_by = SelectField(
        'Sort By',
        choices=[
            ('release_date_desc', 'Release Date (Newest)'),
            ('release_date_asc', 'Release Date (Oldest)'),
            ('study_id', 'Study ID')
        ],
        default='release_date_desc'
    )

    submit = SubmitField('Search')