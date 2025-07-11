### 1. **Изменение названия события при отключенной рассылке**  
   **Цель:** Проверить возможность изменения имени события и его корректное отображение в условиях запуска связанных рассылок.  
   **Предпосылки:** Событие связано с рассылкой в статусе "Отключена".  
   **Шаги:**  
   1. Открыть страницу редактирования события.  
   2. Изменить значение поля "Название события" на "Новое название".  
   3. Перейти в настройки связанной рассылки и проверить условие запуска.  
   **Ожидаемый результат:** В условии запуска рассылки отображается новое название события.  

---

### 2. **Попытка изменения названия события с активной рассылкой**  
   **Цель:** Убедиться, что редактирование имени события заблокировано при активной рассылке.  
   **Предпосылки:** Событие связано с рассылкой в статусе "Включена в активном режиме".  
   **Шаги:**  
   1. Открыть страницу редактирования события.  
   2. Попытаться изменить поле "Название события".  
   **Ожидаемый результат:** Поле "Название события" недоступно для редактирования.  

---

### 3. **Валидация уникальности идентификатора события**  
   **Цель:** Проверить запрет на использование неуникального идентификатора.  
   **Предпосылки:** Существует событие с идентификатором `event_123`.  
   **Шаги:**  
   1. Открыть страницу редактирования другого события.  
   2. Изменить его идентификатор на `event_123`.  
   **Ожидаемый результат:** Появляется сообщение об ошибке: "Идентификатор должен быть уникальным".  

---

### 4. **Попытка ввода спецсимволов в идентификатор события**  
   **Цель:** Проверить запрет на использование недопустимых символов.  
   **Шаги:**  
   1. Открыть страницу редактирования события.  
   2. Ввести в поле "Идентификатор" значение `event@#!`.  
   **Ожидаемый результат:** Поле подсвечивается красным, появляется сообщение: "Допустимы только латинские буквы, цифры и нижние подчеркивания".  

---

### 5. **Удаление неиспользуемого аргумента**  
   **Цель:** Проверить возможность удаления аргумента, не связанного с макросами.  
   **Предпосылки:** Аргумент не используется в макросах рассылок.  
   **Шаги:**  
   1. Открыть страницу редактирования события.  
   2. Нажать "Удалить" рядом с аргументом.  
   **Ожидаемый результат:** Аргумент исчезает из списка.  

---

### 6. **Попытка удаления аргумента, используемого в макросе**  
   **Цель:** Убедиться, что удаление аргумента, задействованного в рассылке, блокируется.  
   **Предпосылки:** Аргумент используется в макросе рассылки.  
   **Шаги:**  
   1. Открыть страницу редактирования события.  
   2. Нажать "Удалить" рядом с аргументом.  
   **Ожидаемый результат:** Появляется сообщение: "Аргумент используется в рассылке «Название рассылки». Удаление невозможно".  

---

### 7. **Редактирование имени аргумента, используемого в макросе**  
   **Цель:** Проверить возможность изменения названия аргумента без влияния на макросы.  
   **Предпосылки:** Аргумент с идентификатором `discount` используется в макросе.  
   **Шаги:**  
   1. Открыть страницу редактирования события.  
   2. Изменить отображаемое имя аргумента `discount` на "Размер скидки".  
   3. Перейти в макросы связанной рассылки.  
   **Ожидаемый результат:** В макросах используется идентификатор `discount`, но отображается новое имя "Размер скидки".  

---

### 8. **Попытка изменения идентификатора аргумента, связанного с макросом**  
   **Цель:** Убедиться, что изменение идентификатора аргумента блокируется.  
   **Предпосылки:** Аргумент с идентификатором `code` используется в макросе.  
   **Шаги:**  
   1. Открыть страницу редактирования события.  
   2. Попытаться изменить идентификатор аргумента `code` на `promo_code`.  
   **Ожидаемый результат:** Поле "Идентификатор аргумента" недоступно для редактирования.  

---

### 9. **Проверка блокировки изменения типа аргумента**  
   **Цель:** Убедиться, что тип аргумента нельзя изменить после создания.  
   **Шаги:**  
   1. Открыть страницу редактирования события.  
   2. Попытаться изменить тип аргумента с `decimal` на `string`.  
   **Ожидаемый результат:** Поле "Тип аргумента" недоступно для редактирования.  

---

### 10. **Попытка редактирования события с активной рассылкой**  
   **Цель:** Проверить блокировку всех полей при активной рассылке.  
   **Предпосылки:** Связанная рассылка в статусе "Включена в активном режиме".  
   **Шаги:**  
   1. Открыть страницу редактирования события.  
   2. Попытаться изменить любое поле.  
   **Ожидаемый результат:** Все поля недоступны для редактирования.  

---

### 11. **Автоматическое сохранение изменений имени события**  
   **Цель:** Проверить мгновенное сохранение изменений без явного подтверждения.  
   **Шаги:**  
   1. Открыть страницу редактирования события.  
   2. Изменить название события.  
   3. Обновить страницу.  
   **Ожидаемый результат:** Новое название сохраняется после обновления страницы.  

---

### 12. **Обработка конфликта идентификаторов при редактировании**  
   **Цель:** Проверить реакцию на конфликт идентификаторов при сохранении.  
   **Предпосылки:** Существует событие с идентификатором `event_456`.  
   **Шаги:**  
   1. Открыть страницу редактирования другого события.  
   2. Изменить его идентификатор на `event_456`.  
   **Ожидаемый результат:** Появляется сообщение: "Идентификатор уже занят".  

---

### 13. **Ввод значения аргумента типа date через календарь**  
   **Цель:** Проверить использование календаря для аргумента типа `date`.  
   **Шаги:**  
   1. На странице тестовой генерации события выбрать аргумент типа `date`.  
   2. Нажать на поле ввода.  
   **Ожидаемый результат:** Открывается календарь для выбора даты.  

---

### 14. **Попытка ввода строки в аргумент типа decimal**  
   **Цель:** Убедиться, что поле `decimal` не принимает буквы.  
   **Шаги:**  
   1. На странице тестовой генерации события выбрать аргумент типа `decimal`.  
   2. Ввести значение `abc`.  
   **Ожидаемый результат:** Поле не принимает ввод, значение остается пустым.  

---

### 15. **Удаление события с неактивными рассылками**  
   **Цель:** Проверить запрет удаления события, связанного с рассылками.  
   **Предпосылки:** Событие используется в рассылке в статусе "Отключена".  
   **Шаги:**  
   1. Открыть страницу события.  
   2. Нажать "Удалить событие".  
   **Ожидаемый результат:** Появляется сообщение: "Событие используется в рассылке. Удаление невозможно".  

---

Каждый сценарий проверяет конкретное поведение, описанное в документации, без дублирования функциональности.