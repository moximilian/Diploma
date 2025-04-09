<template>
    <div class="auth-form">
        <div class="page-title">Вход</div>
        <FormView displayName="login" action="edit">
            <template #form-bottom="{ entity }">
                <div class="form-bottom-column">
                    <BaseBtn @click="authorize(entity)">Войти</BaseBtn>
                    Или
                    <div id="auth-bottom"></div>
                    <div id="auth-bottom2"></div>
                </div>
            </template>
        </FormView>
    </div>
</template>

<script>
import { jwtDecode } from 'jwt-decode'
import { GOOGLE_CLIENT_ID, YANDEX_CLIENT_ID } from '@/api/api.settings'
export default {
    data() {
        return {
            GOOGLE_CLIENT_ID,
            YANDEX_CLIENT_ID,
        }
    },
    methods: {
        authorize(entity) {
            this.$api.auth.login({ ...entity }, res => {
                if (res?.detail) return
                this.$ls.token = res.access_token
                this.$ls.current_user = res.user_id
                this.$store.commit('setUser', res.user_id)
                this.$router.replace('/home')
            })
        },
        async initGoogleAuth() {
            await this.loadBtnScript('https://accounts.google.com/gsi/client?hl=ru')
            try {
                /* eslint-disable no-undef */
                await google.accounts.id.initialize({
                    client_id: GOOGLE_CLIENT_ID,
                    callback: ({ credential }) => {
                        const userData = jwtDecode(credential)
                        const password = this.transformPassword(
                            `${userData.sub}-${userData.email.ucFirst()}`
                        )
                        this.$api.auth.register(
                            {
                                name: userData.given_name,
                                surname: userData.family_name,
                                login: userData.email,
                                password,
                                password_confirm: password,
                                role_name: 'student',
                                is_external_auth: true,
                            },
                            () => {
                                this.authorize({
                                    login: userData.email,
                                    password: password,
                                })
                            }
                        )
                    },
                    response_type: 'token',
                    scope: 'https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email	openid',
                    ux_mode: 'popup',
                })
                google.accounts.id.renderButton(document.getElementById('auth-bottom2'), {
                    theme: 'outline',
                    size: 'large',
                    locale: 'ru',
                })
                google.accounts.id.prompt() // also display the One Tap dialog
                /* eslint-enable no-undef */
            } catch (error) {
                console.error('Google auth error:', error)
            }
        },
        async initYandexAuth() {
            /* eslint-disable no-undef */
            await this.loadBtnScript(
                'https://yastatic.net/s3/passport-sdk/autofill/v1/sdk-suggest-with-polyfills-latest.js'
            )
            try {
                const { handler } = await YaAuthSuggest.init(
                    /* eslint-enable no-undef */
                    {
                        client_id: YANDEX_CLIENT_ID,
                        response_type: 'token',
                        redirect_uri: 'http://localhost:1024/auth/yandex-callback',
                        display: 'page',
                    },
                    null,
                    {
                        display: 'page',
                        view: 'button',
                        parentId: 'auth-bottom',
                        buttonView: 'main',
                        buttonTheme: 'light',
                        buttonSize: 'm',
                        buttonBorderRadius: 8,
                    }
                )
                await handler()
            } catch (error) {
                console.error('Yandex auth error:', error)
            }
        },
        loadBtnScript(path) {
            return new Promise((resolve, reject) => {
                const script = document.createElement('script')
                script.src = path
                script.onload = resolve
                script.onerror = reject
                document.body.appendChild(script)
            })
        },
        transformPassword(uuid) {
            return uuid.replaceAll('.', '').replaceAll('_', '-')
        },
    },
    created() {
        if (![null, '', undefined].includes(this.$ls.token)) {
            this.$router.replace('/home')
            return
        }
        this.initYandexAuth()
        this.initGoogleAuth()
        this.$ls.subscribe('yandex_user_data', () => {
            const userData = JSON.parse(this.$ls.getItemDecrypt('yandex_user_data'))
            const password = this.transformPassword(userData.psuid)
            this.$api.auth.register(
                {
                    name: userData.first_name,
                    surname: userData.last_name,
                    login: userData.login,
                    password,
                    password_confirm: password,
                    role_name: 'student',
                    is_external_auth: true,
                },
                () => {
                    this.authorize({
                        login: userData.login,
                        password: password,
                    })
                }
            )
        })
    },
}
</script>
