import LocalStorage from './LocalStorage.js'
const ls = new LocalStorage()
const registerDisplay = [
    {
        display: 'StringField',
        props: { title: 'Имя', name: 'name', value: '', required: true, type: 'text' },
    },
    {
        display: 'StringField',
        props: { title: 'Фамилия', name: 'surname', value: '', required: true, type: 'text' },
    },
    {
        display: 'StringField',
        props: { title: 'Логин', name: 'login', value: '', required: true, type: 'text' },
    },
    {
        display: 'PasswordField',
        props: { title: 'Пароль', name: 'password', value: '', required: true, type: 'password' },
    },
    {
        display: 'PasswordField',
        props: {
            name: 'password_confirm',

            title: 'Повторите пароль',
            value: '',
            required: true,
            type: 'password',
        },
        same: 'password',
    },
    {
        display: 'SelectField',
        props: {
            title: 'Я собираюсь быть',
            value: 'Обучающимся',
            name: 'role_name',
            required: true,
            // options: ['student', 'teacher'],
            options: [{ student: 'Обучающимся' }, { teacher: 'Преподавателем' }],
        },
    },
]

const loginDisplay = [
    {
        display: 'StringField',
        props: { title: 'Логин', name: 'login', value: '', required: true, type: 'text' },
    },
    {
        display: 'PasswordField',
        props: { title: 'Пароль', name: 'password', value: '', required: true, type: 'password' },
    },
]

const passwordChangeDisplay = [
    {
        display: 'PasswordField',
        props: {
            name: 'current_password',
            title: 'Текущий пароль',
            value: '',
            required: true,
        },
    },
    {
        display: 'PasswordField',
        props: {
            name: 'new_password',
            title: 'Новый пароль',
            value: '',
            required: true,
        },
    },
    {
        display: 'PasswordField',
        props: {
            name: 'new_password_confirm',
            title: 'Повторите пароль',
            value: '',
            required: true,
        },
    },
]

const userDisplay = [
    {
        display: 'StringField',
        props: {
            title: 'Логин',
            name: 'login',
            value: '',
            required: true,
            disabled: true,
            type: 'text',
        },
    },
    {
        display: 'StringField',
        props: { title: 'Имя', name: 'name', value: '', required: false, type: 'text' },
    },
    {
        display: 'StringField',
        props: { title: 'Фамилия', name: 'surname', value: '', required: true, type: 'text' },
    },
    {
        display: 'StringField',
        props: { title: 'Отчество', name: 'last_name', value: '', required: false, type: 'text' },
    },
    {
        display: 'StringField',
        props: {
            title: 'Зарегистрирован',
            name: 'registered_at',
            value: '',
            required: true,
            disabled: true,
            type: 'text',
        },
    },
]

const groupsDisplay = [
    {
        display: 'StringField',
        props: {
            name: 'creator_id',
            value: ls.current_user,
            disabled: true,
            required: true,
            title: 'Автор',
            type: 'text',
        },
    },
    {
        display: 'StringField',
        props: { title: 'Название группы', name: 'name', value: '', required: true, type: 'text' },
    },
    {
        display: 'StringField',
        props: { title: 'Описание', name: 'description', value: '', required: false, type: 'text' },
    },
    {
        display: 'SwitchField',
        props: { title: 'Открытая группа', name: 'is_open', value: true, required: true, type: 'checkbox' },
    },
    {
        display: 'StringField',
        props: {
            title: 'Максимальное кол-во участников',
            name: 'max_participants_count',
            value: 8,
            required: true,
            type: 'number',
        },
    },
]



//filters

const groupsFilter = [
    {
        display: 'StringField',
        props: {
            name: 'name',
            placeholder: 'Поиск',
            type: 'text',
        },
        condition: '='
    },
    {
        display: 'RadioField',
        props: {
            name: 'creator_id',
            title: 'Автор',
            options: {[ls._current_user]: "Я", [false]: 'Другие'},
            value: ls._current_user
        },
        condition: '='

    },
    {
        display: 'RadioField',
        props: {
            name: 'is_open',
            title: 'Тип группы',
            options: {[true]: 'Открытые', [false]: 'Закрытые'},
            value: "true"
        },
        condition: '='
    },
    {
        display: 'RangeField',
        props: {
            name: 'max_participants_count',
            title: 'Кол-во участников',
            value: [0, 8],
            min: 0,
            max: 45,
        },
        condition: 'between'
    },
]

export default {
    registerDisplay,
    loginDisplay,
    userDisplay,
    groupsDisplay,
    passwordChangeDisplay,

    groupsFilter,
}
