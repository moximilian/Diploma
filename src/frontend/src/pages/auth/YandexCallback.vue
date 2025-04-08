<template>
    <div></div>
</template>
<script>
export default {
    mounted() {
        const url = new URL(window.location.href)
        const hash = url.hash.substring(1)
        const params = new URLSearchParams(hash)
        const accessToken = params.get('access_token')
        if (!accessToken) return
        this.$api.auth.yandexGetData(accessToken, 'json', data => {
            this.$ls.setItemEncrypt('yandex_user_data', JSON.stringify(data))
            window.close()
        })
    },
}
</script>
