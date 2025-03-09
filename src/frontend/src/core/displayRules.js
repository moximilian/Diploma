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
            title: 'Создатель',
            type: 'text',
        },
    },
    {
        display: 'StringField',
        props: { title: 'Название', name: 'name', value: '', required: true, type: 'text' },
    },
    {
        display: 'StringField',
        props: { title: 'Описание', name: 'description', value: '', required: false, type: 'text' },
    },
    {
        display: 'StringField',
        props: { title: 'Открыта', name: 'is_open', value: true, required: true, type: 'checkbox' },
    },
    {
        display: 'StringField',
        props: {
            title: 'Максимальное количество участников',
            name: 'max_participants_count',
            value: 8,
            required: true,
            type: 'number',
        },
    },
]
export default {
    registerDisplay,
    loginDisplay,

    userDisplay,
    groupsDisplay,
    passwordChangeDisplay,
}
