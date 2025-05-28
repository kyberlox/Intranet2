<template>
	<div class="admin-toolbar">
		<div class="admin-toolbar__search-container">
			<input type="text"
				   tabindex="1"
				   placeholder="Фильтр + поиск"
				   class="admin-toolbar__search-input" />
		</div>
		<div class="admin-toolbar__actions">
			<div class="admin-toolbar__buttons">
				<RouterLink :to="'name'"
							id="lists-title-action-add"
							class="admin-toolbar__button admin-toolbar__button--primary">
					Добавить
				</RouterLink>
			</div>
		</div>
	</div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { RouterLink } from 'vue-router';

export default defineComponent({
	setup() {
		return {}
	}
})
</script>

<style scoped>
.admin-toolbar {
	display: flex;
	flex-direction: row;
	justify-content: space-evenly
}

.admin-toolbar__search-container {
	display: flex;
	flex-wrap: nowrap;
	align-items: center;
	position: relative;
	height: 39px;
	border: 1px solid #c8d1d6;
	border-radius: 2px;
	background: #fff;
	box-sizing: border-box;
	outline: 0;
	z-index: 1;
	overflow: hidden;
	float: left;
	margin-top: 18px;
	margin-bottom: 18px;
	min-width: 420px;
}

.admin-toolbar__search-input {
	position: relative;
	z-index: 1;
	box-sizing: border-box;
	padding: 0 55px 0 16px;
	width: 100%;
	height: 30px;
	outline: 0;
	border: 0;
	border-radius: 2px;
	background-color: #fff;
}



.admin-toolbar__actions {
	display: flex;
	justify-content: flex-end;
	align-items: center;
}

.admin-toolbar__button {
	padding: 0 15px;
	height: 39px;
	line-height: 39px;
	text-decoration: none;
	display: inline-block;
	cursor: pointer;
	border-radius: 5px;

	&:hover {
		transform: scale(1.02);
		background: #1f6c86;
	}
}

.admin-toolbar__button--primary {
	background-color: #3bc8f5;
	color: #fff;
}
</style>
