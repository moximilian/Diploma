<template>
    <div class="form-container">
        <div class="form" v-if="displayRule">
            <slot name="form-top"> </slot>
            <div class="label-type-field" v-for="(field, index) of displayRule" :key="index">
                <component
                    :is="displayComponent(field)"
                    v-if="canModify"
                    v-bind="field.props"
                    @changeValue="onChangeValue"
                >
                    <template #beforeInput>
                        <span>{{ field.props.title }}</span>
                    </template>
                </component>
                <ShowValueField v-else v-bind="field.props" />
            </div>
            <slot name="form-bottom" :entity="entity"> </slot>
        </div>
    </div>
</template>
<script>
import displayRules from '@/core/displayRules'
export default {
    props: {
        displayName: { type: String, default: () => '' },
        defaults: { type: Object, default: null },
        canModify: { type: Boolean, default: () => false },
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
        componentProps(field) {
            return { ...field.props }
        },
        displayComponent(field) {
            return field.display
        },
        onChangeValue(value, name) {
            this.entity[name] = value
        },
    },
}
</script>
