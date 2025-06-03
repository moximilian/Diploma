<template>
    <NestedPage title="Редактирование слота">
        <template #page-content>
            <FormView v-if="entity" action="edit" :defaults="entity" displayName="slots">
                <template #form-bottom="{ entity }">
                    <BaseBtn :outline="true" @click="$router.back()">Назад</BaseBtn>
                    <BaseBtn v-if="!isStudent" @click="async () => await saveSlot(entity)"
                        >Сохранить</BaseBtn
                    >
                </template>
            </FormView>
        </template>
    </NestedPage>
</template>
<script>
export default {
    data() {
        return {
            slotId: null,
            entity: null,
        }
    },
    computed: {
        isStudent() {
            return this.$store.getters.isStudent
        },
        groupName() {
            return this.$route.query.name ?? ''
        },
    },
    methods: {
        async saveSlot(entity) {
            const { body, ok } = await this.$api.slots.update({
                ...entity,
                id: this.slotId,
                repeat_id: this.entity.repeat_id,
            })
            if (!ok) return
            this.$router.replace(`/slots/show/${body.id}`)
        },
    },
    async created() {
        this.slotId = this.$route.params.id
        if (!this.slotId) {
            return console.error('slot ID is not given')
        }
        const { body, ok } = await this.$api.slots.one({ id: this.slotId })
        if (!ok) return console.error('Error during API call')
        this.entity = body
    },
}
</script>
