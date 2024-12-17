<template>
    <div class="form" v-if="displayRule">
        <div class="label-type-field" v-for="(field, index) of displayRule" :key="index">
            <span>{{ field.props.name }}</span>
            <component
                :is="displayComponent(field)"
                v-bind="field.props"
                @changeValue="onChangeValue"
            >
            </component>
        </div>
        <slot name="form-bottom" :entity="entity" :isValid="isValidForm">
            <BaseBtn v-if="isEdit" @click="$emit('onSave', entity)" :disabled="!isValidForm">
                Save
            </BaseBtn>
        </slot>
    </div>
</template>
<script>
import displayRules from '@/core/displayRules'
export default {
    emits: ['onSave'],
    props: {
        displayName: { type: String, default: () => '' },
        onlyEdit: { type: Boolean, default: () => false },
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
        displayNameR() {
            return this.displayName + 'Display'
        },
        displayRule() {
            return this.displayRules?.[this.displayNameR] ?? null
        },
        isShow() {
            return this.action === 'show' && this.onlyEdit
        },
        isEdit() {
            return this.action === 'edit' || this.onlyEdit
        },
        action() {
            return this.$route?.params?.action
        },
        isValidForm() {
            return this.requiredForm && this.sameValidationForm
        },
    },
    methods: {
        // @todo: переписать валидацию, сделать её на каждое поле а не на всю форму сразу
        // checkValidation() {
        //     this.displayRule?.map(rule => {
        //         // same validation
        //         if (rule.same) {
        //             let isSameValid = this.entity[rule.same] === this.entity[rule.props.name]
        //             rule.props.isValid = isSameValid
        //             this.sameValidationForm = isSameValid
        //         }
        //         // required validation
        //         const isValidRequired = rule.props.required ? !!this.entity?.[rule.props.name] : true;
        //         rule.props.isValid = isValidRequired
        //         this.requiredForm = this.requiredForm && isValidRequired
        //     })
        // },
        componentProps(field) {
            return { ...field.props }
        },
        displayComponent(field) {
            return this.isShow ? 'span' : field.display
        },
        onChangeValue(value, name) {
            this.entity[name] = value
            // this.checkValidation()
        },
    },
}
</script>
