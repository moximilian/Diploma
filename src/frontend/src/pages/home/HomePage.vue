<template>
    <TimeTable />
</template>

<script>
export default {
    data() {
        return {
            items: {},
        }
    },
    computed: {
        accessToken() {
            return this.$ls.token
        },
    },
}
</script>
