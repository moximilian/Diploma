<template>
    <FormBase :displayName="displayName" :defaults="defaultValues" :canModify="canModify">
        <template #form-bottom="{ entity }">
            <slot name="form-bottom" :entity="entity" :onSave="onSave">
                <BaseBtn :outline="true" v-if="!isEdit" @click="toList"> Назад</BaseBtn>
                <BaseBtn v-if="canModify" :disabled="!isValidForm" @click="onSave(entity)">
                    Сохранить
                </BaseBtn>
                <BaseBtn v-if="isShow && entityId" @click="toEdit"> Изменить</BaseBtn>
            </slot>
        </template>
    </FormBase>
</template>
<script>
import FormBase from './FormBase.vue'
import displayRules from '@/core/displayRules'
export default {
    emits: ['onSave'],
    components: { FormBase },
    props: {
        displayName: { type: String, default: () => '' },
        defaults: { type: Object, default: null },
        action: { type: String, default: () => this.$route?.params?.action ?? 'show' },
    },
    data() {
        return {
            entity: {},
            displayRules,
            sameValidationForm: true,
            requiredForm: true,
        }
    },
    computed: {
        isShow() {
            return this.action === 'show'
        },
        isNew() {
            return this.action === 'new'
        },
        canModify() {
            return this.isNew || this.action === 'edit'
        },
        isValidForm() {
            return this.requiredForm && this.sameValidationForm
        },
        entityId() {
            return this.$route.params?.id ?? null
        },
        defaultValues() {
            return !this.isNew && this.defaults
        },
    },
    methods: {
        onSave(entity) {
            this.$emit('onSave', entity)
        },
        toList() {
            this.$router.push(`/${this.displayName}/list`)
        },
        toEdit() {
            const editPath = this.$route.path.replace('show', 'edit')
            this.entityId && this.$router.push({ path: `${editPath}` })
        },
    },
}
</script>
