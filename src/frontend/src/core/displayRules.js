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
            value: 'student',
            name: 'role_name',
            required: true,
            options: [
                { key: 'student', value: 'Обучающимся' },
                { key: 'teacher', value: 'Преподавателем' },
            ],
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
        displayName: 'users',
        fieldKey: 'id',
        showName: ['name', 'surname', 'last_name'],
        localKeyName: 'creator_id',
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
        props: {
            title: 'Открытая группа',
            name: 'is_open',
            value: true,
            required: true,
            type: 'checkbox',
        },
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

const participantsDisplay = [
    ...userDisplay,
    {
        display: 'StringField',
        props: {
            title: 'Группа',
            name: 'group_id',
            value: '',
            required: false,
            disabled: true,
            type: 'number',
        },
    },
]

const enter_requestsDisplay = [
    {
        display: 'StringField',
        props: {
            name: 'fio',
            disabled: true,
            required: true,
            title: 'ФИО',
            type: 'text',
        },
        displayName: 'users',
        fieldKey: 'id',
        showName: ['name', 'surname', 'last_name'],
        localKeyName: 'user_id',
    },
    {
        display: 'StringField',
        props: {
            name: 'login',
            disabled: true,
            required: true,
            title: 'Логин',
            type: 'text',
        },
        displayName: 'users',
        fieldKey: 'id',
        showName: 'login',
        localKeyName: 'user_id',
    },
    {
        display: 'StringField',
        props: {
            title: 'Время отправки',
            name: 'datetime',
            value: '',
            required: false,
            disabled: true,
        },
    },
    {
        display: 'StringField',
        props: {
            title: 'Время отправки',
            name: 'datetime',
            value: '',
            required: false,
            disabled: true,
        },
    },
    {
        display: 'StringField',
        props: {
            title: 'Принят в группу',
            name: 'is_approved',
            value: '',
            required: false,
            disabled: true,
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
        condition: '=',
    },
    {
        display: 'RadioField',
        props: {
            name: 'creator_id',
            title: 'Автор',
            options: { [ls._current_user]: 'Я', [false]: 'Другие' },
            value: ls._current_user,
        },
        condition: '=',
    },
    {
        display: 'RadioField',
        props: {
            name: 'is_open',
            title: 'Тип группы',
            options: { [true]: 'Открытые', [false]: 'Закрытые' },
            value: 'true',
        },
        condition: '=',
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
        condition: 'between',
    },
]

export default {
    registerDisplay,
    loginDisplay,
    userDisplay,
    groupsDisplay,
    passwordChangeDisplay,
    participantsDisplay,
    groupsFilter,
    enter_requestsDisplay,
}
