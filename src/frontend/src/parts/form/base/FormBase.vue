<template>
    <div class="form" v-if="displayRule">
        <slot name="form-top"> </slot>
        <div class="label-type-field" v-for="(field, index) of displayRule" :key="index">
            <span>{{ field.props.name }}</span>
            <component
                :is="displayComponent(field)"
                v-if="isEdit"
                v-bind="field.props"
                @changeValue="onChangeValue"
            />
            <ShowValueField v-else v-bind="field.props" />
        </div>
        <slot name="form-bottom" :entity="entity" :isValid="isValidForm">
            <BaseBtn v-if="isEdit" @click="onSave" :disabled="!isValidForm"> Save </BaseBtn>
            <BaseBtn v-if="isShow && entityId" @click="toEdit"> Edit </BaseBtn>
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
        defaults: { type: Object, default: null },
        defaultAction: { type: String, default: null },
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
            let displayRule = this.displayRules?.[this.displayNameR] ?? null
            if (displayRule && !this.isNew) displayRule = this.injectWithValues(displayRule)
            return displayRule
        },
        isShow() {
            return this.action === 'show' || this.onlyEdit
        },
        isNew() {
            return this.action === 'new'
        },
        isEdit() {
            return this.isNew || this.action === 'edit' || this.onlyEdit
        },
        action() {
            return this.defaultAction ?? this.$route?.params?.action
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
        toEdit() {
            const editPath = this.$route.path.replace('show', 'edit')
            this.entityId && this.$router.push({ path: `${editPath}` })
        },
        componentProps(field) {
            return { ...field.props }
        },
        displayComponent(field) {
            return field.display
        },
        onChangeValue(value, name) {
            this.entity[name] = value
            // this.checkValidation()
        },
    },
}
</script>
