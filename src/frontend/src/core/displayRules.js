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
        props: { name: 'lastname', value: '', required: false, type: 'text' },
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
export default {
    registerDisplay,
    loginDisplay,
}
