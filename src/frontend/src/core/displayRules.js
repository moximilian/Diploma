import LocalStorage from './LocalStorage.js'
const ls = new LocalStorage()
const registerDisplay = [
    {
        display: 'InputField',
        props: { name: 'name', value: '', required: true, type: 'text' },
    },
    {
        display: 'InputField',
        props: { name: 'surname', value: '', required: true, type: 'text' },
    },
    {
        display: 'InputField',
        props: { name: 'last_name', value: '', required: false, type: 'text' },
    },
    {
        display: 'InputField',
        props: { name: 'login', value: '', required: true, type: 'text' },
    },
    {
        display: 'InputField',
        props: { name: 'password', value: '', required: true, type: 'password' },
    },
    {
        display: 'InputField',
        props: {
            name: 'password_confirm',
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
        props: { name: 'login', value: '', required: true, type: 'text' },
    },
    {
        display: 'InputField',
        props: { name: 'password', value: '', required: true, type: 'password' },
    },
]

const userDisplay = [
    {
        display: 'InputField',
        props: { name: 'name', value: '', required: false, type: 'text' },
    },
    {
        display: 'InputField',
        props: { name: 'surname', value: '', required: true, type: 'text' },
    },
    {
        display: 'InputField',
        props: { name: 'last_name', value: '', required: false, type: 'text' },
    },
    {
        display: 'InputField',
        props: { name: 'login', value: '', required: true, disabled: true, type: 'text' },
    },
    {
        display: 'InputField',
        props: { name: 'registered_at', value: '', required: true, disabled: true, type: 'text' },
    },
]

const groupsDisplay =  [
    {
        display: 'InputField',
        props: { name: 'creator_id', value: ls.current_user, disabled: true, required: true, type: 'text' },
    },
    {
        display: 'InputField',
        props: { name: 'name', value: '', required: true, type: 'text' },
    },
    {
        display: 'InputField',
        props: { name: 'description', value: '', required: false, type: 'text' },
    },
    {
        display: 'InputField',
        props: { name: 'is_open', value: true, required: true, type: 'checkbox' },
    },
    {
        display: 'InputField',
        props: { name: 'max_participants_count', value: 8, required: true, type: 'number' },
    },
]
export default {
    registerDisplay,
    loginDisplay,

    userDisplay,
    groupsDisplay,
}
