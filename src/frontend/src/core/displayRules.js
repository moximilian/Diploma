import LocalStorage from './LocalStorage.js'
const ls = new LocalStorage()
const registerDisplay = [
    {
        display: 'InputField',
        props: { title: 'Имя', name: 'name', value: '', required: true, type: 'text' },
    },
    {
        display: 'InputField',
        props: { title: 'Фамилия', name: 'surname', value: '', required: true, type: 'text' },
    },
    {
        display: 'InputField',
        props: { title: 'Отчество', name: 'last_name', value: '', required: false, type: 'text' },
    },
    {
        display: 'InputField',
        props: { title: 'Логин', name: 'login', value: '', required: true, type: 'text' },
    },
    {
        display: 'InputField',
        props: { title: 'Пароль', name: 'password', value: '', required: true, type: 'password' },
    },
    {
        display: 'InputField',
        props: {
            name: 'password_confirm',
            title: 'Повторите пароль',
            value: '',
            required: true,
            type: 'password',
        },
        same: 'password',
    },
]

const loginDisplay = [
    {
        display: 'InputField',
        props: { title: 'Логин', name: 'login', value: '', required: true, type: 'text' },
    },
    {
        display: 'InputField',
        props: { title: 'Пароль', name: 'password', value: '', required: true, type: 'password', },
    },
]

const userDisplay = [
    {
        display: 'InputField',
        props: { title: 'Имя', name: 'name', value: '', required: false, type: 'text' },
    },
    {
        display: 'InputField',
        props: { title: 'Фамилия', name: 'surname', value: '', required: true, type: 'text' },
    },
    {
        display: 'InputField',
        props: { title: 'Отчество', name: 'last_name', value: '', required: false, type: 'text' },
    },
    {
        display: 'InputField',
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
        display: 'InputField',
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
        display: 'InputField',
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
        display: 'InputField',
        props: { title: 'Название', name: 'name', value: '', required: true, type: 'text' },
    },
    {
        display: 'InputField',
        props: { title: 'Описание', name: 'description', value: '', required: false, type: 'text' },
    },
    {
        display: 'InputField',
        props: { title: 'Открыта', name: 'is_open', value: true, required: true, type: 'checkbox' },
    },
    {
        display: 'InputField',
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
}
