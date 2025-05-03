<template>
    <NestedPage title="Создать слот" v-if="!isStudent">
        <template #page-content>
            <FormView action="new" displayName="slots" @onSave="createSlot"> </FormView>
        </template>
    </NestedPage>
</template>
<script>
export default {
    data() {
        return {
            entity: null,
        }
    },
    computed: {
        isStudent() {
            return this.$store.getters.isStudent
        },
    },
    methods: {
        async createSlot(entity) {
            const { body, ok } = await this.$api.slots.insert({ ...entity })
            if (!ok) return
            this.$router.replace(`/slots/show/${body[0].id}`)
        },
    },
}
</script>
