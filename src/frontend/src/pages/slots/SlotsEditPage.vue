<template>
    <NestedPage title="Редактирование слота">
        <template #page-content>
            <FormView v-if="entity" action="edit" :defaults="entity" displayName="slots">
                <template #form-bottom="{ entity }">
                    <BaseBtn v-if="!isStudent" @click="saveSlot(entity)">Сохранить</BaseBtn>
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
        saveSlot(entity) {
            this.$api.slots.update(
                { ...entity, id: this.slotId, repeat_id: this.entity.repeat_id },
                res => {
                    if (res.detail) return
                    this.$router.replace(`/slots/show/${res.id}`)
                }
            )
        },
    },
    created() {
        this.slotId = this.$route.params.id
        if (!this.slotId) {
            return console.error('slot ID is not given')
        }
        this.$api.slots.one({ id: this.slotId }, res => {
            if (res.detail) return console.error('Error during API call')
            this.entity = res
        })
    },
}
</script>
