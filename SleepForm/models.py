from datetime import datetime
from time import time
from django.db import models


class SleepQuestionnaire(models.Model):
    class Difficulty(models.IntegerChoices):
        NONE = 0, 'Nenhuma dificuldade'
        MILD = 1, 'Um problema leve'
        MODERATE = 2, 'Um problema razoável'
        SEVERE = 3, 'Um grande problema'

        @classmethod
        def get_value(cls, label):
            """Return the integer value of a given choice label."""
            for value, name in cls.choices:
                if name == label:
                    return value
            return None

    class Quality(models.IntegerChoices):
        VERY_GOOD = 4, 'Muito boa'
        GOOD = 3, 'Boa'
        FAIR = 2, 'Ruim'
        POOR = 1, 'Muito ruim'

        @classmethod
        def get_value(cls, label):
            """Return the integer value of a given choice label."""
            for value, name in cls.choices:
                if name == label:
                    return value
            return None
    
    class Frequency(models.IntegerChoices): 
        NONE = 0, 'Nenhuma no último mês'
        LESS_THAN_ONCE_A_WEEK = 1, 'Menos de 1 vez/semana'
        ONCE_OR_TWICE_A_WEEK = 2, '1 ou 2 vezes/semana'    
        VERY_OFTEN = 3, '3 ou mais vezes/semana'

        @classmethod
        def get_value(cls, label):
            """Return the integer value of a given choice label."""
            for value, name in cls.choices:
                if name == label:
                    return value
            return None

    class Partner(models.IntegerChoices):
        NO = 0, 'Não'
        PARTNER_IN_OTHER_ROOM = 1, 'Parceiro ou colega, mas em outro quarto'
        PARTNER_IN_SAME_ROOM = 2, 'Parceiro no mesmo quarto, mas não na mesma cama'
        PARTNER_IN_SAME_BED = 3, 'Parceiro na mesma cama'

        @classmethod
        def get_value(cls, label):
            """Return the integer value of a given choice label."""
            for value, name in cls.choices:
                if name == label:
                    return value
            return None

    # Basic sleep information
    bedtime = models.TimeField(verbose_name="Hora usual de deitar")
    time_to_sleep = models.PositiveIntegerField(verbose_name="Minutos para dormir")
    wakeup_time = models.TimeField(verbose_name="Hora usual de levantar")
    sleep_hours = models.FloatField(verbose_name="Horas de sono por noite")
    
    # Sleep difficulties
    difficulty_falling_asleep = models.IntegerField(
        max_length=1, choices=Frequency.choices,
        verbose_name="Não conseguiu adormecer em até 30 minutos"
    )
    difficulty_staying_asleep = models.IntegerField(
        max_length=1, choices=Frequency.choices,
        verbose_name="Acordou no meio da noite ou de manhã cedo"
    )
    bathroom_visits = models.IntegerField(
        max_length=1, choices=Frequency.choices,
        verbose_name="Precisou levantar para ir ao banheiro"
    )
    breathing_difficulty = models.IntegerField(
        max_length=1, choices=Frequency.choices,
        verbose_name="Não conseguiu respirar confortavelmente"
    )
    coughing_snoring = models.IntegerField(
        max_length=1, choices=Frequency.choices,
        verbose_name="Tossiu ou roncou forte"
    )
    felt_cold = models.IntegerField(
        max_length=1, choices=Frequency.choices,
        verbose_name="Sentiu muito frio"
    )
    felt_hot = models.IntegerField(
        max_length=1, choices=Frequency.choices,
        verbose_name="Sentiu muito calor"
    )
    bad_dreams = models.IntegerField(
        max_length=1, choices=Frequency.choices,
        verbose_name="Teve sonhos ruins"
    )
    pain = models.IntegerField(
        max_length=1, choices=Frequency.choices,
        verbose_name="Teve dor"
    )
    other_reason = models.TextField(
        blank=True, null=True,
        verbose_name="Outra(s) razão(ões), por favor descreva"
    )
    other_reason_frequency = models.IntegerField(
        max_length=1, choices=Frequency.choices, blank=True, null=True,
        verbose_name="Frequência da outra razão"
    )
    
    # General sleep evaluation
    sleep_quality = models.IntegerField(
        max_length=1, choices=Quality.choices,
        verbose_name="Qualidade geral do sono"
    )
    medication_use = models.IntegerField(
        max_length=1, choices=Frequency.choices,
        verbose_name="Uso de medicamento para dormir"
    )
    daytime_sleepiness = models.IntegerField(
        max_length=1, choices=Frequency.choices,
        verbose_name="Dificuldade de ficar acordado durante atividades"
    )
    enthusiasm_difficulty = models.IntegerField(
        max_length=1, choices=Difficulty.choices,
        verbose_name="Dificuldade em manter entusiasmo"
    )
    
    # Partner information
    has_partner = models.IntegerField(
        max_length=1, choices=Partner.choices,
        verbose_name="Tem parceiro/colega de quarto?"
    )
    partner_snoring = models.IntegerField(
        max_length=1, choices=Frequency.choices, blank=True, null=True,
        verbose_name="Ronco forte (observado por parceiro)"
    )
    partner_breathing_pauses = models.IntegerField(
        max_length=1, choices=Frequency.choices, blank=True, null=True,
        verbose_name="Longas paradas na respiração (observado por parceiro)"
    )
    partner_leg_movements = models.IntegerField(
        max_length=1, choices=Frequency.choices, blank=True, null=True,
        verbose_name="Contrações/puxões nas pernas (observado por parceiro)"
    )
    partner_confusion = models.IntegerField(
        max_length=1, choices=Frequency.choices, blank=True, null=True,
        verbose_name="Episódios de desorientação (observado por parceiro)"
    )
    partner_other_issues = models.TextField(
        blank=True, null=True,
        verbose_name="Outras alterações observadas (descreva)"
    )
    partner_other_frequency = models.IntegerField(
        max_length=1, choices=Frequency.choices, blank=True, null=True,
        verbose_name="Frequência das outras alterações"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Questionário de sono de {self.created_at.date()}"
            
    

