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
        display: 'SelectField',
        props: {
            title: 'Я являюсь',
            value: 'student',
            name: 'role_name',
            required: true,
            options: [
                { key: 'student', value: 'Обучающимся' },
                { key: 'teacher', value: 'Преподавателем' },
            ],
        },
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
const eventsDisplay = [
    {
        display: 'StringField',
        props: {
            name: 'name',
            required: true,
            title: 'Название',
            placeholder: '',
            type: 'text',
        },
    },
    {
        display: 'StringField',
        props: {
            name: 'description',
            required: true,
            title: 'Описание',
            type: 'text',
        },
    },
    {
        display: 'StringField',
        props: {
            name: 'price',
            required: true,
            title: 'Цена',
            type: 'number',
        },
    },
    {
        display: 'DatePicker',
        props: {
            name: 'start_date',
            required: true,
            title: 'Дата',
            type: 'text',
        },
    },
    {
        display: 'StringField',
        props: {
            name: 'start_time',
            title: 'Начало',
            required: true,
        },
    },
    {
        display: 'StringField',
        props: {
            name: 'end_time',
            title: 'Конец',
            required: true,
        },
    },
    {
        display: 'SelectField',
        props: {
            name: 'weekdays',
            title: 'Дни недели',
            value: [],
            options: [
                { key: 1, value: 'Понедельник' },
                { key: 2, value: 'Вторник' },
                { key: 3, value: 'Среда' },
                { key: 4, value: 'Четверг' },
                { key: 5, value: 'Пятница' },
                { key: 6, value: 'Суббота' },
                { key: 7, value: 'Воскресенье' },
            ],
            multiple: true,
        },
    },
    {
        display: 'SelectField',
        props: {
            name: 'months',
            title: 'Месяцы',
            value: [],
            options: [
                { key: 1, value: 'Январь' },
                { key: 2, value: 'Февраль' },
                { key: 3, value: 'Март' },
                { key: 4, value: 'Апрель' },
                { key: 5, value: 'Май' },
                { key: 6, value: 'Июнь' },
                { key: 7, value: 'Июль' },
                { key: 8, value: 'Август' },
                { key: 9, value: 'Сентябрь' },
                { key: 10, value: 'Октябрь' },
                { key: 11, value: 'Ноябрь' },
                { key: 12, value: 'Декабрь' },
            ],
            multiple: true,
        },
    },
    {
        display: 'StringField',
        props: {
            name: 'group_id',
            disabled: true,
            required: true,
            title: 'Группа',
            type: 'text',
        },
        displayName: 'groups',
        fieldKey: 'id',
        showName: 'name',
        localKeyName: 'id',
    },
]

const slotsDisplay = [
    ...eventsDisplay.filter(field => field.props.name !== 'group_id'),
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
        displayName: 'users',
        fieldKey: 'id',
        showName: ['name', 'surname', 'last_name'],
        localKeyName: 'creator_id',
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

const groupsTeacherFilter = [
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


const groupsStudentFilter = [
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
            name: 'is_open',
            title: 'Тип группы',
            options: { [true]: 'Открытые', [false]: 'Закрытые' },
            value: 'true',
        },
        condition: '=',
    },
    {
        display: 'RadioField',
        props: {
            name: 'is_currrent_participant',
            title: 'Уже состою',
            options: { [true]: 'Да', [false]: 'Нет' },
            value: [true],
        },
        condition: '=',
    },
]
const slotsStudentFilter = [
    {
        display: 'SelectSearchFieldModel',
        props: {
            name: 'creator_id',
            modelName: 'users',
            title: 'Организатор индивидуальных занятий',
            fieldKey: 'id',
            showFieldName: 'login',
            showFormat: (key) => {
                return key?.login ?? key
            },
            defaultWheres: [{
                column: 'role_name',
                condition: '=',
                value: 'teacher',
            }]
        },
        condition: '=',
    },
    {
        display: 'SelectSearchFieldModel',
        props: {
            name: 'group_id',
            modelName: 'groups',
            title: 'Мои группы',
            fieldKey: 'name',
            showFieldName: 'name',
            multiple: true,
            showFormat: (key) => {
                return key?.name ?? key
            },
            defaultWheres: [{
                column: 'is_currrent_participant',
                condition: '=',
                value: true
            }]
        },
        condition: '=',
    }
]

export default {
    registerDisplay,
    loginDisplay,
    userDisplay,
    groupsDisplay,
    passwordChangeDisplay,
    participantsDisplay,
    groupsTeacherFilter,
    enter_requestsDisplay,
    groupsStudentFilter,
    eventsDisplay,
    slotsDisplay,
    slotsStudentFilter
}
