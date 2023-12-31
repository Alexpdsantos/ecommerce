from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from . import models

from pprint import pprint

class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by = 6

    """
    def get(self, *args, **kwargs):
        return HttpResponse('Listar')
    paginate_by = 10"""


class DetalheProduto(DetailView):
    model = models.Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'

# Carrinho contém configuração de sessions, a fim de manter o mesmo
# ativo por até 7 dias(conf salva em Settings.py)


class AdicionarAoCarrinho(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get('HTTP_REFERER',
                                             reverse('produto:lista'))
        variacao_id = self.request.GET.get('vid')
        if not variacao_id:
            messages.error(
                self.request, 'Produto não existe'
            )
            return redirect(http_referer)
        variacao = get_object_or_404(models.Variacao, id=variacao_id)
        produto = variacao.produto

        produto_id = produto.id
        produto_nome = produto.nome
        variacao_nome = variacao.nome or ''
        variacao_id = variacao.id
        preco_unitario = variacao.preco
        preco_unitario_promocional = variacao.preco_promocional
        quantidade = 1
        slug = produto.slug
        imagem = produto.imagem

        if imagem:
            imagem = imagem.name
        else:
            imagem = ''

        if variacao.estoque < 1:
            messages.error(
                self.request,
                'Estoque Insuficiente'
            )
            return redirect(http_referer)

        # Carrinho por sua vez é um "Dicionário" que está ligado à sessão,
        # que está salva do lado do servidor- Na Base de dados em formato JSON
        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()

        carrinho = self.request.session['carrinho']

        if variacao_id in carrinho:
            quantidade_carrinho = carrinho[variacao_id]['quantidade']
            quantidade_carrinho +=1
            if variacao_estoque < quantidade_carrinho:
                messages.warning(
                    self.request,
                    f'Estoque Insuficiente, Adicionada a quantidade existente'
                )
            quantidade_carrinho = variacao_estoque
            carrinho[variacao_id]['quantidade'] = quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo'] = preco_unitario * quantidade_carrinho 
            carrinho[variacao_id]['preco_quantitativo_promocional'] = preco_unitario_promocional * quantidade_carrinho 

        
        else:
            carrinho[variacao_id] = {
                'produto_id': produto_id,
                'produto_nome':produto_nome,
                'variacao_nome':variacao_nome,
                'variacao_id':variacao_id,
                'preco_unitario':preco_unitario,
                'preco_unitario_promocional':preco_unitario_promocional,
                'preco_quantitativo': preco_unitario,
                'preco_quantitativo_promocional':preco_unitario_promocional,
                'quantidade': 1,
                'slug':slug,
                'imagem':imagem,
            }
        self.request.session.save()
        pprint(carrinho)
        return HttpResponse(f'{variacao.produto}{variacao.nome}')


class RemoverDoCarrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Remover carrinho')


class Carrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Carrinho')
    
class Finalizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Finalizar')
