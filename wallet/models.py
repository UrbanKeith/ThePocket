from django.contrib.auth.models import User
from django.db import models


class PeriodType(models.Model):
    """
    Модель типов периода (день, неделя, месяц, квартал, год)
    TODO: Добавить возможность ограничивать или проверять период по его типу. Возможно добавить количество дней в периода, например в неделе не больше 7 дней
    """
    name = models.CharField(max_length=30)


class Period(models.Model):
    name = models.CharField(max_length=30)
    date_start = models.DateField()
    date_end = models.DateField()
    period_type = models.ForeignKey(PeriodType, on_delete=models.PROTECT)


class Wallet(models.Model):
    """
    Модель кошелька
    """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50, null=True, blank=True)
    params = models.JSONField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)


class IncomeCategory(models.Model):
    """
    Модель категорий дохода
    """
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100, null=True, blank=True)
    params = models.JSONField()
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)


class IncomeEntry(models.Model):
    """
    Модель записей о доходах
    """
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True, null=True)
    value = models.DecimalField(max_digits=12, decimal_places=2)
    datetime = models.DateTimeField()
    category = models.ForeignKey(IncomeCategory, on_delete=models.PROTECT)


class IncomePeriodPlan(models.Model):
    """
    Модель периода планирования доходов
    """
    name = models.CharField(max_length=30)
    period = models.ForeignKey(Period, on_delete=models.PROTECT)


class IncomePlan(models.Model):
    """
    Модель плана доходов на определенный период
    """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=30)  # Статус плана (уже прошел, исполняется, будущий)
    value = models.DecimalField(max_digits=12, decimal_places=2)
    plan_period = models.ForeignKey(IncomePeriodPlan, on_delete=models.PROTECT)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)


class ExpenseCategory(models.Model):
    """
    Модель категорий расходов
    """
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100, null=True, blank=True)
    params = models.JSONField()
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)


class ExpenseEntry(models.Model):
    """
    Модель записей о расходах
    """
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True, null=True)
    value = models.DecimalField(max_digits=12, decimal_places=2)
    datetime = models.DateTimeField()
    category = models.ForeignKey(ExpenseCategory, on_delete=models.PROTECT)


class ExpensePeriodPlan(models.Model):
    """
    Модель периода планирования расходов
    """
    name = models.CharField(max_length=30)
    period = models.ForeignKey(Period, on_delete=models.PROTECT)


class ExpensePlan(models.Model):
    """
    Модель плана расходов на определенный период
    """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=30)  # Статус плана (уже прошел, исполняется, будущий)
    value = models.DecimalField(max_digits=12, decimal_places=2)
    plan_period = models.ForeignKey(IncomePeriodPlan, on_delete=models.PROTECT)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)


class Bill(models.Model):
    """
    Модель результата за определенный период
    TODO: Возможно создавать на основе плана при завершении очередного плана или сделать только периодическим
    """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    period = models.ForeignKey(Period, on_delete=models.PROTECT)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
