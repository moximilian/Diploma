<template>
    <NestedPage title="Создать слот" v-if="!isStudent">
        <template #page-content>
            <FormView action="new" displayName="slots" @onSave="entity => createSlot(entity)">
            </FormView>
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
        createSlot(entity) {
            this.$api.slots.insert({ ...entity }, res => {
                if (res.detail) return
                this.$router.replace(`/slots/show/${res[0].id}`)
            })
        },
    },
}
</script>
