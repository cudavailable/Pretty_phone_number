from django.db import models

# Create your models here.
class Department(models.Model):
    """ 部门表 """
    dname = models.CharField(verbose_name='部门名', max_length=32)

    def __str__(self):
        return self.dname

class UserInfo(models.Model):
    """ 员工表 """
    name = models.CharField(verbose_name='员工名', max_length=32)
    pwd = models.CharField(verbose_name='密码', max_length=64)
    age = models.IntegerField(verbose_name='年龄')
    sal = models.DecimalField(verbose_name='用户薪资',max_digits=10, decimal_places=2, default=0)
    crt_time = models.DateField(verbose_name='入职时间')

    # 级联删除 注意不需要命名成'dept_id' Django会自动附加'_id' 而且会更方便关联表操作
    dept = models.ForeignKey(verbose_name='部门', to='Department', to_field='id', on_delete=models.CASCADE)
    # 置空
    #dept = models.ForeignKey(to='Department', to_fields='id', null=True, blank=True, on_delete=models.SET_NULL)

    gender_choices = (
        (1, '男'),
        (2, '女')
    )
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices)

class PrettyNum(models.Model):
    """靓号表"""
    mobile = models.CharField(verbose_name='手机号', max_length=11)
    price = models.IntegerField(verbose_name='价格', default=0)

    level_choices = (
        (1, '1级'),
        (2, '2级'),
        (3, '3级'),
        (4, '4级'),
    )
    level = models.SmallIntegerField(verbose_name='级别', choices=level_choices, default=1)

    status_choices = (
        (1, '已占用'),
        (2, '未使用'),
    )
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choices, default=2)

class Admin(models.Model):
    """管理员表"""
    username = models.CharField(verbose_name='管理员名称', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)


