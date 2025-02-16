<template>
    <FormBase 
        :displayName="displayName" 
        :defaults="defaults"
        :canModify="canModify"
    >
        <template #form-bottom="{ entity }">
            <slot name="form-bottom" 
                :entity="entity" 
                :onSave="onSave"
            >
                <BaseBtn 
                    v-if="canModify" 
                    :disabled="!isValidForm"
                    @click="onSave" 
                > Сохранить </BaseBtn>
                <BaseBtn 
                    v-if="isShow && entityId" 
                    @click="toEdit"
                > Изменить</BaseBtn>
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
    },
    methods: {
        injectWithValues(enryRule) {
            this.defaults &&
                enryRule.map(rule => {
                    rule.props.value = this.defaults[rule.props.name]
                })
            return enryRule
        },
        onSave() {
            this.$emit('onSave', this.entity)
        },
        toEdit() {
            const editPath = this.$route.path.replace('show', 'edit')
            this.entityId && this.$router.push({ path: `${editPath}` })
        },
    },
}
</script>
