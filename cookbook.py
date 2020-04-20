from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text, ForeignKey, Table
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///cook_book_project.db')
Base = declarative_base(bind=engine)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

posts_tags_table = Table(
    'tags_posts',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True),
)




class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(30), nullable=False)

    posts = relationship('Post', back_populates='user')

    def __repr__(self):
        return f'<User # {self.id} name {self.username}>'


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    title = Column(String(40), nullable=False)
    text = Column(Text, nullable=False)
    is_published = Column(Boolean, nullable=False, default=False)

    user = relationship('User', back_populates='posts')
    tags = relationship(
        'Tag',
        secondary=posts_tags_table,
        back_populates='posts'
    )

    def __repr__(self):
        return f'<Post # {self.id} by {self.user_id} {self.title}>'


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)

    posts = relationship(
        'Post',
        secondary=posts_tags_table,
        back_populates='tags'
    )

    def __repr__(self):
        return f'<Tag # {self.id} {self.name}>'





def create_post_user_tags():
    session = Session()

    user = User(username='Third')
    session.add(user)
    session.commit()
    session.refresh(user)

    post = Post(user_id=user.id, title='Post_new', text='My new post in there')
    session.add(post)
    session.commit()
    session.refresh(post)

    post.tags.append(Tag(name='Пирог'))
    session.commit()


def create_users_posts():
    session = Session()

    user = User(username='First')
    session.add(user)
    session.flush(session)
    post1 = Post(user_id=user.id, title='Грибной пирог', text="""
    Пора грибов настала. 
    Собирать их приятно, да. А вот потом возни с ними много.
    По мне так - очень много. Но... знаю людей, которым и это не помеха: 
    и собирают, и чистят,и солят-маринуют, и жарят на все лады и вкусы. 
    И, конечно,фотографируются с этим лесным даром, а потом друзей дразнят.
    Но есть и из грибов замечательные рецепты. Быстрые, я бы сказала, ну 
    или достаточно быстрые. Например Пирог с грибами. На мой взгляд, очень
    аппетитный. Автор рецепта Алина Фомичева утверждает, что такой пирог 
    никогда не надоест. И готовить его рекомендует из шампиньонов. А мне тут 
    подумалось, что можно такой пирог и из белых грибов приготовить. А почему 
    нет в грибную-то пору?
    Нам понадобится:
    Мука пшеничная 250 гр;
    Сливочное масло 150 гр;
    Яйцо 3 шт;
    Соль 1 ч. л;
    Шампиньоны 500 гр;
    Лук 1 шт;
    Сметана 100 гр;
    Сливки (10%) 100 мл;
    Растительное масло для жарки.
    Готовим:
    
    Просеиваем муку в глубокую емкость. Добавляем одно яйцо, ½ ч. л. соли, 
    размягченное масло и хорошо замешиваем тесто.
    Затем заворачиваем в пищевую пленку и ставим в холодильник на 30 минут.
    Чистим и нарезаем грибы. Мелко нарезаем лук.
    Разогреваем сковороду с растительным маслом, кладем лук и обжариваем до 
    полупрозрачности.
    Добавляем грибы и жарим до выпаривания жидкости.
    В миске смешиваем сметану и 2 яйца. Добавляем ½ ч. л соли, сливки и 
    тщательно перемешиваем.
    Форму для выпечки смазываем маслом и распределяем равномерно тесто, 
    формируя бортики.
    Выкладываем грибы с луком и заливаем соусом.
    Заливка из сливок, сметаны и грибов после приготовления будет слегка 
    влажной и нежной.
    Разогреваем духовку до 180 С и ставим на 25-30 минут.
    Всё. Наслаждаемся новым вкусом!
    """)

    user = User(username='Second')
    session.add(user)
    session.flush(session)
    post2 = Post(user_id=user.id, title='Суп с пельмешками', text="""
    Суп из мясного бульона с крошечными домашними пельменями с мясом. 
    Почему «ложечный» суп? 
    Потому что мастерство в данном случае ложкой оценивается: 
    чем больше пельменей помещается в ложке, тем искуснее хозяйка.
    
    Ароматный наваристый бульон, крошечные, будто игрушечные, пельмешки и 
    много свежей зелени. Приготовление супа, конечно, требует определённых 
    временных затрат, но дело того сто́ит. В итоге получается невероятная 
    вкуснятина!
    Варим къашыкъ аш (ложечный суп) - знаменитый крымско-татарский суп с 
    пельменями. И да, дорогие девушки, не забываем - у хорошей хозяйки должно
    помещаться не менее 12 пельмешек на ложку.
    
    Для рецепта вам потребуется:
    для мясного бульона:
    говяжья или телячья грудинка
    овощи
    для теста:
    вода - 150 мл
    молоко - 150 мл
    соль - 1 ч.л. (с горкой)
    мука - 700г
    яйцо - 1 шт.
    для начинки:
    мясной фарш (говядина, баранина или телятина) - 500г
    репчатый лук - 1 шт.
    соль, перец - по вкусу.
    Рецепт приготовления:
     Шаг 01
    Варим прозрачный бульон из говяжьей или телячьей грудинки и овощей. 
    Затем замешиваем тесто из смеси воды с молоком, чайной ложки с горкой 
    соли, муки и 1 яйца.
    Шаг 02
    Тесто оставить на 30 минут, потом ещё раз хорошо обмять и оставить ещё 
    на 30 минут, прикрыв от высыхания.
    Шаг 03
    Делаем фарш из говядины и баранины, просто говядины или телятины. У меня 
    готовый говяжий фарш 500, туда мелко крошим 1 луковицу большую. 
    Можно даже блендером вжикнуть. Посолить, поперчить на свой вкус.
    Шаг 04
    Тесто отлежалось. Отрезаем небольшой кусочек и раскатываем тонко и 
    режем на квадратики 1,5Х2 см.
    Шаг 05
    Кладём на каждый квадратик фарша размером с горошинку и залепляем. Тесто 
    очень быстро сохнет, поэтому прикрываем мокрой марлей.
    Шаг 06
    Процесс лепки пельменей долгий, медитативный.
    Шаг 07
    Бульон уже сварился. Мясо вынимаем, его потом можно будет на что-то другое 
    пустить или просто съесть с хреном или горчицей. Овощи выбрасываем, они 
    отдали свой аромат. Ставим рядом кастрюлю с кипятком и вначале обвариваем 
    в кипятке 30 секунд пельмени для того, чтобы бульон был не мутный. А потом
    варим обычным манером пельмешки в бульоне. Кладём в тарелку с много зелени.
    У меня всего 10 штук поместилось в ложку. Значит крупные, надо мельче. 
    Добавляем сметанку или турецкий йогурт.    
    Приятного!""")

    session.add(post1)
    session.add(post2)

    session.commit()
    session.close()


def show_existing_tags():
    session = Session()
    q_tags = session.query(Tag)
    tag = q_tags.first()
    print(tag.posts)
    print(tag)
    session.close()


def add_tags_to_posts():
    session = Session()
    tag = session.query(Tag).first()
    post = session.query(Post).first()
    post.tags.append(tag)
    session.commit()

    print(post, post.tags)
    print(tag, tag.posts)


def show_join():
    """
    :return:
    """
    session = Session()
    q = session.query(
        User,
    ).join(
        Post,
        User.id == Post.user_id,
    ).filter(
        Post.tags.any(Tag.id == 2)
    )
    print(q)
    print(q.all())


def show_methods():
    session = Session()
    q = session.query(Tag).filter(Tag.id == 1)
    print(q)
    print(type(q))
    print(list(q))
    print(q.all())
    q = session.query(Tag.name).filter(Tag.id.in_([1, 2, 4]))
    print(q)
    print(type(q))
    print(list(q))
    print(q.all())
    q = session.query(Tag.name).filter(Tag.id.in_([1, 2, 4]))
    print(q)
    print(type(q))
    print(list(q))
    print([r for r, in q.all()])

    user_ok = session.query(User.username).filter(User.id == 1)
    user = user_ok.one()
    print(user)

    res_username = user_ok.scalar()
    print('username:', res_username)
    pass


def main():
    """
    :return:
    """
    Base.metadata.create_all()
    print('засолка')
    create_post_user_tags()
    print('засолка2')
    create_users_posts()
    print('засолка3')
    show_existing_tags()
    print('засолка4')
    add_tags_to_posts()
    show_join()
    show_methods()


if __name__ == '__main__':
    main()
