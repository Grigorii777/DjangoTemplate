## Выборка (часто используемые)

* `all()` — вся таблица.
* `filter(**kwargs)` — отбор.
* `exclude(**kwargs)` — исключение.
* `order_by("field", "-field")` — сортировка.
* `distinct()` — уникальные строки.
* `values("f1","f2")` / `values_list("f", flat=True)` — проекция.
* `only("f1","f2")` / `defer("f3")` — выбрать/отложить поля.
* `select_related("fk")` — JOIN для FK/O2O.
* `prefetch_related("m2m","fk_set")` — отдельный запрос + merge.

> // Use `select_related` for single-valued relations; `prefetch_related` for many-valued.

## Получение одной/части

* `get(**kwargs)` — одна запись или ошибка.
* `first()` / `last()` — первый/последний.
* `exists()` — проверка наличия.
* `count()` — количество.
* `earliest("dt")` / `latest("dt")` — по дате.

> // `exists()` is O(1) and faster than `count()>0`.

## Создание/изменение/удаление

* `create(**fields)` — создать.
* `get_or_create(defaults=..., **lookup)` — найти/создать.
* `update_or_create(defaults=..., **lookup)` — обновить/создать.
* `update(**fields)` — массовое обновление (без `save()`).
* `delete()` — удалить (qs или объект).
* `bulk_create(objs, batch_size=...)` — пачка вставок.
* `bulk_update(objs, ["f1","f2"])` — пачка обновлений.

> // `update()` bypasses model `save()`/signals; be careful.

## Связи (M2M/FK обратки)

* `<obj>.m2m.add(*objs|ids)` / `remove(...)` / `clear()` / `set([...])`.
* `<obj>.related_set.all()` — обратный менеджер FK.

> // Prefer `set([...])` to replace entire M2M atomically.

## Лукапы (в `filter()/exclude()`)

* Сравнение: `exact`, `iexact`, `in`, `gt/gte/lt/lte`, `range`, `isnull`.
* Текст: `contains/icontains`, `startswith/istartswith`, `endswith/iendswith`, `regex/iregex`.
* Даты/время: `date`, `year`, `month`, `day`, `hour`, `week`, `quarter`.

> // Case-insensitive: use `i*` variants (e.g., `icontains`).

## Аннотации/агрегации

* `annotate(...)` — поля на лету.
* `aggregate(...)` — итог по QS.
* Часто: `Count`, `Sum`, `Avg`, `Min`, `Max`.

```python
# Example (EN): group by status with counts
from orders.models import Order
Order.objects.values("status").annotate(cnt=Count("id")).order_by("-cnt")
```

## Выражения (Expression API)

* `Q(...)` / `~Q(...)` — сложные условия (AND/OR/NOT).
* `F("field")` — операции на уровне БД (инкремент, сравнение).
* `Case/When` — условные поля.
* `Subquery(...)`, `Exists(...)`, `OuterRef("field")` — подзапросы.

```python
# Example (EN): atomic increment
Order.objects.filter(pk=pk).update(amount=F("amount") + 10)
```

## Транзакции/блокировки

* `transaction.atomic()` — явная транзакция.
* `transaction.on_commit(func)` — колбек после коммита.
* `select_for_update(nowait=True|skip_locked=True)` — блокировка строк.

> // Wrap multi-step writes in `atomic()` to keep data consistent.

## Пагинация (часто в списках)

* `Paginator(qs, per_page)` → `page_obj = paginator.get_page(page_num)`.

---

### Мини-шаблон для 80% кейсов (EN comments)

```python
# Read list with performance
from orders.models import Order
qs = (Order.objects
      .select_related("customer")      # FK join
      .prefetch_related("items")       # M2M/Reverse FK
      .only("id","number","status","amount","created_at")  # narrow columns
      .filter(status__in=["paid","shipped"])
      .order_by("-created_at"))

# Aggregation example
stats = Order.objects.aggregate(total=Sum("amount"), n=Count("id"))

# Update example (atomic increment)
Order.objects.filter(id=oid).update(amount=F("amount") + 100)

# Create-or-get
obj, created = Order.objects.get_or_create(number="A-100", defaults={"status":"new"})
```

