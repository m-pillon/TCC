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
            
    def calculate_total_score(self):
        """
        Calculates the total score by summing all integer response values.
        Handles null/blank fields appropriately.
        """
        score_fields = [
            # Sleep difficulties (Frequency choices)
            'difficulty_falling_asleep',
            'difficulty_staying_asleep',
            'bathroom_visits',
            'breathing_difficulty',
            'coughing_snoring',
            'felt_cold',
            'felt_hot',
            'bad_dreams',
            'pain',
            'other_reason_frequency',
            
            # General evaluation
            'medication_use',
            'daytime_sleepiness',
            
            # Partner-related fields
            'partner_snoring',
            'partner_breathing_pauses',
            'partner_leg_movements',
            'partner_confusion',
            'partner_other_frequency',
        ]
        
        # Special fields that need inverse scoring (higher number = better)
        inverse_score_fields = {
            'sleep_quality': True,  # Very Good=4 is better than Very Bad=1
            'enthusiasm_difficulty': False,
            'has_partner': False,  # Partner status isn't really a score
        }
        
        total = 0
        
        # Sum all regular score fields
        for field in score_fields:
            value = getattr(self, field)
            if value is not None:
                total += int(value)
        
        # Handle special fields
        if self.sleep_quality is not None:
            # Invert quality score (4=best becomes 1, 1=worst becomes 4)
            total += (4 - int(self.sleep_quality) + 1)
            
        if self.enthusiasm_difficulty is not None:
            # Count difficulty as-is (0=none, 3=severe)
            total += int(self.enthusiasm_difficulty)
        
        return total
    
    def get_score_interpretation(self):
        """
        Provides an interpretation of the total score
        """
        total = self.calculate_total_score()
        
        if total <= 15:
            return "Good sleep health"
        elif 15 < total <= 30:
            return "Mild sleep disturbance"
        elif 30 < total <= 45:
            return "Moderate sleep disturbance"
        else:
            return "Severe sleep disturbance"
    
    def get_detailed_scores(self):
        """
        Returns a dictionary with component scores and total
        """
        return {
            'sleep_difficulties': self._sum_difficulty_scores(),
            'sleep_quality': self._get_quality_score(),
            'daytime_impact': self._get_daytime_scores(),
            'total': self.calculate_total_score(),
            'interpretation': self.get_score_interpretation()
        }
    
    def _sum_difficulty_scores(self):
        """Helper method to sum all sleep difficulty scores"""
        difficulty_fields = [
            'difficulty_falling_asleep',
            'difficulty_staying_asleep',
            'bathroom_visits',
            'breathing_difficulty',
            'coughing_snoring',
            'felt_cold',
            'felt_hot',
            'bad_dreams',
            'pain',
            'other_reason_frequency'
        ]
        return sum(
            int(getattr(self, field)) 
            for field in difficulty_fields 
            if getattr(self, field) is not None
        )
    
    def _get_quality_score(self):
        """Helper method for sleep quality component"""
        if self.sleep_quality is None:
            return None
        return (4 - int(self.sleep_quality) + 1)  # Inverted scoring
    
    def _get_daytime_scores(self):
        """Helper method for daytime impact component"""
        daytime_fields = [
            'daytime_sleepiness',
            'enthusiasm_difficulty',
            'medication_use'
        ]
        return sum(
            int(getattr(self, field))
            for field in daytime_fields
            if getattr(self, field) is not None
        )

